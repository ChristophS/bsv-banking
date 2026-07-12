from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
from dataclasses import replace
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Iterable, Sequence

from banking_readonly.config import AppConfig
from banking_readonly.balance_snapshot import load_balance_snapshot
from banking_readonly.exporter import ALLOWED_ACCOUNTS
from banking_readonly.security import ensure_private_directory, protect_file

from .database import (
    NORMALIZED_COLUMNS,
    connect_database,
    import_parsed_file,
    manual_balance_correction_for,
    recalculate_account_balances,
    transaction_count,
    transaction_rows,
    transaction_rows_by_ids,
)
from .models import AccountDefinition, ParsedFile
from .parsers import detect_export_account, parse_export
from .rules import (
    ClassificationRule,
    CompletionRule,
    apply_rule_pipeline,
    connect_rules_database,
    load_classification_rules,
    load_completion_rules,
)


@dataclass(frozen=True)
class ImportSummary:
    runs: int
    source_files: int
    parsed_rows: int
    new_transactions: int
    existing_transactions: int
    total_transactions: int
    database_path: Path
    normalized_path: Path


@dataclass(frozen=True)
class HistoricalAccountSummary:
    provider: str
    account_name: str
    account_number: str
    source_files: int
    unique_transactions: int
    overlapping_transactions: int
    date_from: str
    date_to: str


@dataclass(frozen=True)
class HistoricalImportSummary:
    import_summary: ImportSummary
    recognized_files: int
    ignored_files: int
    accounts: tuple[HistoricalAccountSummary, ...]


def ingest_export_run(
    config: AppConfig,
    paths: Sequence[Path],
    store_root: Path,
) -> ImportSummary:
    if not paths:
        raise ValueError("Keine Exportdateien zum Importieren vorhanden.")
    run_dir = paths[0].parent
    if any(path.parent != run_dir for path in paths):
        raise ValueError("Alle Exportdateien muessen aus demselben Lauf stammen.")
    return _ingest_runs(config, (run_dir,), store_root)


def import_existing_exports(
    configs: Sequence[AppConfig],
    store_root: Path,
) -> ImportSummary:
    totals = _empty_summary(store_root)
    for config in configs:
        runs = _discover_runs(config.export.output_dir)
        current = _ingest_runs(config, runs, store_root)
        totals = ImportSummary(
            runs=totals.runs + current.runs,
            source_files=totals.source_files + current.source_files,
            parsed_rows=totals.parsed_rows + current.parsed_rows,
            new_transactions=(
                totals.new_transactions + current.new_transactions
            ),
            existing_transactions=(
                totals.existing_transactions + current.existing_transactions
            ),
            total_transactions=current.total_transactions,
            database_path=current.database_path,
            normalized_path=current.normalized_path,
        )
    return totals


def import_transaction_directory(
    configs: Sequence[AppConfig],
    source_root: Path,
    store_root: Path,
) -> HistoricalImportSummary:
    source_root = source_root.expanduser().resolve()
    if not source_root.is_dir():
        raise FileNotFoundError(
            f"Importverzeichnis nicht gefunden: {source_root}"
        )

    account_definitions = {}
    for config in configs:
        for account in _accounts(config).values():
            account_definitions[(account.provider, account.number)] = account

    candidates = sorted(
        path
        for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() == ".csv"
    )
    parsed_files = []
    ignored_files = 0
    for path in candidates:
        identity = detect_export_account(path)
        if identity is None:
            ignored_files += 1
            continue
        account = account_definitions.get(identity)
        if account is None:
            raise ValueError(
                "Transaktionsauszug gehoert zu keinem konfigurierten Konto: "
                f"{path} ({identity[0]} {identity[1]})"
            )
        parsed_files.append(parse_export(path, account))

    if not parsed_files:
        raise ValueError(
            f"Keine unterstuetzten Transaktionsauszuege in {source_root}."
        )

    account_summaries = _historical_account_summaries(parsed_files)
    _validate_overlapping_balances(parsed_files)
    import_summary = _import_historical_files(parsed_files, store_root)
    return HistoricalImportSummary(
        import_summary=import_summary,
        recognized_files=len(parsed_files),
        ignored_files=ignored_files,
        accounts=account_summaries,
    )


def _ingest_runs(
    config: AppConfig,
    run_dirs: Iterable[Path],
    store_root: Path,
) -> ImportSummary:
    layout = _layout(store_root)
    for path in layout.values():
        ensure_private_directory(path if path.suffix == "" else path.parent)

    accounts = _accounts(config)
    connection = connect_database(layout["database"])
    rules_connection = connect_rules_database(layout["rules_database"])
    rules = load_classification_rules(rules_connection)
    completion_rules = load_completion_rules(rules_connection)
    runs = source_files = parsed_rows = new_transactions = existing = 0
    try:
        for run_dir in sorted(run_dirs):
            parsed_files = _parse_run(config, run_dir, accounts, connection)
            if not parsed_files:
                continue
            run_summary = _archive_and_import_run(
                connection,
                parsed_files,
                run_dir.name,
                layout,
                rules,
                completion_rules,
            )
            runs += 1
            source_files += len(parsed_files)
            parsed_rows += sum(len(item.transactions) for item in parsed_files)
            new_transactions += run_summary["new_transactions"]
            existing += run_summary["existing_transactions"]
        apply_rule_pipeline(connection, rules, completion_rules)
        connection.commit()
        _write_master_csv(connection, layout["master_csv"])
        total = transaction_count(connection)
    finally:
        connection.close()
        rules_connection.close()
    protect_file(layout["database"])
    protect_file(layout["rules_database"])
    return ImportSummary(
        runs=runs,
        source_files=source_files,
        parsed_rows=parsed_rows,
        new_transactions=new_transactions,
        existing_transactions=existing,
        total_transactions=total,
        database_path=layout["database"],
        normalized_path=layout["master_csv"],
    )


def _import_historical_files(
    parsed_files: Sequence[ParsedFile],
    store_root: Path,
) -> ImportSummary:
    layout = _layout(store_root)
    for path in layout.values():
        ensure_private_directory(path if path.suffix == "" else path.parent)

    connection = connect_database(layout["database"])
    rules_connection = connect_rules_database(layout["rules_database"])
    rules = load_classification_rules(rules_connection)
    completion_rules = load_completion_rules(rules_connection)
    imported = []
    new_transactions = 0
    existing_transactions = 0
    try:
        for parsed in parsed_files:
            existing_source = connection.execute(
                """
                SELECT file_id, export_run_id, archive_path
                FROM source_files
                WHERE provider = ?
                  AND original_filename = ?
                  AND file_sha256 = ?
                LIMIT 1
                """,
                (
                    parsed.account.provider,
                    parsed.path.name,
                    parsed.sha256,
                ),
            ).fetchone()
            run_id = (
                existing_source["export_run_id"]
                if existing_source is not None
                else _historical_run_id(parsed)
            )
            year, month = _run_year_month(run_id)
            raw_dir = ensure_private_directory(
                layout["raw"]
                / parsed.account.provider
                / year
                / month
                / run_id
            )
            manifest_dir = ensure_private_directory(
                layout["manifests"]
                / parsed.account.provider
                / year
                / month
            )
            normalized_dir = ensure_private_directory(
                layout["normalized_runs"]
                / parsed.account.provider
                / year
                / month
            )
            archive_path = (
                Path(existing_source["archive_path"])
                if existing_source is not None
                else raw_dir / parsed.path.name
            )
            _archive_raw_file(parsed.path, archive_path, parsed.sha256)
            file_id = (
                existing_source["file_id"]
                if existing_source is not None
                else _source_file_id(
                    parsed.account.provider,
                    run_id,
                    parsed.path.name,
                    parsed.sha256,
                )
            )
            new_count, existing_count = import_parsed_file(
                connection,
                parsed,
                file_id,
                run_id,
                parsed.path.resolve(),
                archive_path.resolve(),
            )
            new_transactions += new_count
            existing_transactions += existing_count
            imported.append(
                {
                    "parsed": parsed,
                    "run_id": run_id,
                    "file_id": file_id,
                    "archive_path": archive_path,
                    "manifest_dir": manifest_dir,
                    "normalized_path": normalized_dir / f"{run_id}.csv",
                    "new_transactions": new_count,
                    "existing_transactions": existing_count,
                }
            )

        transaction_ids = sorted(
            {
                transaction.transaction_id
                for parsed in parsed_files
                for transaction in parsed.transactions
            }
        )
        apply_rule_pipeline(
            connection,
            rules,
            completion_rules,
            transaction_ids,
        )
        connection.commit()

        for item in imported:
            parsed = item["parsed"]
            run_transaction_ids = [
                transaction.transaction_id
                for transaction in parsed.transactions
            ]
            _write_transactions_csv(
                item["normalized_path"],
                transaction_rows_by_ids(connection, run_transaction_ids),
            )
            manifest = {
                "manifest_version": 1,
                "provider": parsed.account.provider,
                "export_run_id": item["run_id"],
                "imported_at": datetime.now(timezone.utc).isoformat(),
                "files": [
                    {
                        "filename": parsed.path.name,
                        "file_id": item["file_id"],
                        "sha256": parsed.sha256,
                        "encoding": parsed.encoding,
                        "delimiter": parsed.delimiter,
                        "row_count": len(parsed.transactions),
                        "archive_path": str(
                            item["archive_path"].resolve()
                        ),
                    }
                ],
                "normalized_path": str(
                    item["normalized_path"].resolve()
                ),
                "new_transactions": item["new_transactions"],
                "existing_transactions": item["existing_transactions"],
            }
            _write_manifest_once(
                item["manifest_dir"] / f"{item['run_id']}.json",
                manifest,
            )

        _write_master_csv(connection, layout["master_csv"])
        total = transaction_count(connection)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
        rules_connection.close()

    protect_file(layout["database"])
    protect_file(layout["rules_database"])
    return ImportSummary(
        runs=len(parsed_files),
        source_files=len(parsed_files),
        parsed_rows=sum(len(item.transactions) for item in parsed_files),
        new_transactions=new_transactions,
        existing_transactions=existing_transactions,
        total_transactions=total,
        database_path=layout["database"],
        normalized_path=layout["master_csv"],
    )


def _historical_account_summaries(
    parsed_files: Sequence[ParsedFile],
) -> tuple[HistoricalAccountSummary, ...]:
    grouped: dict[tuple[str, str], list[ParsedFile]] = {}
    for parsed in parsed_files:
        grouped.setdefault(
            (parsed.account.provider, parsed.account.number),
            [],
        ).append(parsed)

    summaries = []
    for items in grouped.values():
        transactions = [
            transaction
            for parsed in items
            for transaction in parsed.transactions
        ]
        transaction_ids = [
            transaction.transaction_id for transaction in transactions
        ]
        dates = [transaction.booking_date for transaction in transactions]
        account = items[0].account
        summaries.append(
            HistoricalAccountSummary(
                provider=account.provider,
                account_name=account.name,
                account_number=account.number,
                source_files=len(items),
                unique_transactions=len(set(transaction_ids)),
                overlapping_transactions=(
                    len(transaction_ids) - len(set(transaction_ids))
                ),
                date_from=min(dates, default=""),
                date_to=max(dates, default=""),
            )
        )
    return tuple(
        sorted(
            summaries,
            key=lambda item: (item.provider, item.account_name),
        )
    )


def _validate_overlapping_balances(
    parsed_files: Sequence[ParsedFile],
) -> None:
    observations: dict[str, int] = {}
    for parsed in parsed_files:
        for transaction in parsed.transactions:
            if transaction.account_balance is None:
                continue
            balance_minor = int(transaction.account_balance * 100)
            existing = observations.setdefault(
                transaction.transaction_id,
                balance_minor,
            )
            if existing != balance_minor:
                raise RuntimeError(
                    "Inkonsistenter Kontostand in ueberlappenden "
                    f"Auszuegen fuer {transaction.transaction_id}: "
                    f"{existing / 100:.2f} statt {balance_minor / 100:.2f}."
                )


def _historical_run_id(parsed: ParsedFile) -> str:
    import re

    matches = [
        match.groups()
        for match in re.finditer(
            r"(?<!\d)(20\d{2})[._-]?(\d{2})[._-]?(\d{2})(?!\d)",
            parsed.path.stem,
        )
    ]
    valid_dates = []
    for groups in matches:
        candidate = "".join(groups)
        try:
            datetime.strptime(candidate, "%Y%m%d")
        except ValueError:
            continue
        valid_dates.append(candidate)
    if valid_dates:
        run_date = valid_dates[-1]
    elif parsed.transactions:
        run_date = max(
            item.booking_date for item in parsed.transactions
        ).replace("-", "")
    else:
        run_date = datetime.fromtimestamp(
            parsed.path.stat().st_mtime,
            tz=timezone.utc,
        ).strftime("%Y%m%d")
    suffix = int(parsed.sha256[:12], 16) % 1_000_000
    return f"{run_date}T000000_{suffix:06d}Z"


def _parse_run(
    config: AppConfig,
    run_dir: Path,
    accounts: dict[str, AccountDefinition],
    connection=None,
) -> tuple[ParsedFile, ...]:
    observations = load_balance_snapshot(run_dir, config.provider)
    expected_numbers = {account.number for account in accounts.values()}
    if observations and set(observations) != expected_numbers:
        raise RuntimeError(
            f"Kontostandsdatei in {run_dir.name} ist unvollstaendig "
            "oder enthaelt unerwartete Konten."
        )

    parsed = []
    for filename, account in accounts.items():
        path = run_dir / filename
        if not path.is_file():
            raise FileNotFoundError(
                f"Exportlauf {run_dir.name} ist unvollstaendig: {filename} fehlt."
            )
        observation = observations.get(account.number)
        if observation is not None:
            if observation.account_name.casefold() != account.name.casefold():
                raise RuntimeError(
                    f"Kontoname in der Kontostandsdatei passt nicht zu "
                    f"{filename}."
                )
            balance_as_of = observation.captured_at.date().isoformat()
            correction = (
                manual_balance_correction_for(
                    connection, account.provider, account.number, balance_as_of
                ) if connection is not None else None
            )
            effective_balance = (
                Decimal(int(correction["balance_minor"])) / Decimal(100)
                if correction is not None else observation.balance
            )
            parsed_file = parse_export(
                    path,
                    account,
                    account_balance=effective_balance,
                    balance_as_of=balance_as_of,
                    balance_currency=observation.currency,
                )
            parsed.append(
                replace(
                    parsed_file,
                    account_balance=observation.balance,
                    observed_account_balance=observation.balance,
                    comparison_account_balance=(effective_balance if correction else None),
                    manual_balance_correction_id=(str(correction["correction_id"]) if correction else None),
                    manual_balance_correction_reason=(str(correction["reason"]) if correction else None),
                )
            )
        else:
            parsed.append(parse_export(path, account))
    return tuple(parsed)


def _archive_and_import_run(
    connection,
    parsed_files: Sequence[ParsedFile],
    run_id: str,
    layout: dict[str, Path],
    rules: Sequence[ClassificationRule],
    completion_rules: Sequence[CompletionRule],
) -> dict[str, int]:
    provider = parsed_files[0].account.provider
    year, month = _run_year_month(run_id)
    raw_dir = ensure_private_directory(
        layout["raw"] / provider / year / month / run_id
    )
    manifest_dir = ensure_private_directory(
        layout["manifests"] / provider / year / month
    )
    normalized_dir = ensure_private_directory(
        layout["normalized_runs"] / provider / year / month
    )

    manifest_files = []
    run_transaction_ids = set()
    new_transactions = 0
    existing_transactions = 0
    for parsed in parsed_files:
        archive_path = raw_dir / parsed.path.name
        _archive_raw_file(parsed.path, archive_path, parsed.sha256)
        file_id = _source_file_id(
            provider,
            run_id,
            parsed.path.name,
            parsed.sha256,
        )
        new_count, existing_count = import_parsed_file(
            connection,
            parsed,
            file_id,
            run_id,
            parsed.path.resolve(),
            archive_path.resolve(),
        )
        new_transactions += new_count
        existing_transactions += existing_count
        for transaction in parsed.transactions:
            run_transaction_ids.add(transaction.transaction_id)
        manifest_files.append(
            {
                "filename": parsed.path.name,
                "file_id": file_id,
                "sha256": parsed.sha256,
                "encoding": parsed.encoding,
                "delimiter": parsed.delimiter,
                "row_count": len(parsed.transactions),
                "archive_path": str(archive_path.resolve()),
                "account_balance": (
                    format(parsed.account_balance, ".2f")
                    if parsed.account_balance is not None
                    else None
                ),
                "balance_currency": parsed.balance_currency,
                "balance_as_of": parsed.balance_as_of,
                "observed_account_balance": (
                    format(parsed.observed_account_balance, ".2f")
                    if parsed.observed_account_balance is not None else None
                ),
                "manual_balance_correction": (
                    {"correction_id": parsed.manual_balance_correction_id,
                     "balance": format(parsed.comparison_account_balance, ".2f"),
                     "balance_as_of": parsed.balance_as_of,
                     "reason": parsed.manual_balance_correction_reason}
                    if parsed.manual_balance_correction_id else None
                ),
            }
        )

    recalculated_accounts = set()
    for parsed in parsed_files:
        account_key = (
            parsed.account.provider,
            parsed.account.number,
        )
        if (
            parsed.account_balance is not None
            and account_key not in recalculated_accounts
        ):
            recalculate_account_balances(
                connection,
                parsed.account.provider,
                parsed.account.number,
                (
                    int(parsed.comparison_account_balance * 100)
                    if parsed.comparison_account_balance is not None
                    else None
                ),
            )
            recalculated_accounts.add(account_key)

    apply_rule_pipeline(
        connection,
        rules,
        completion_rules,
        sorted(run_transaction_ids),
    )
    connection.commit()
    normalized_path = normalized_dir / f"{run_id}.csv"
    _write_transactions_csv(
        normalized_path,
        transaction_rows_by_ids(
            connection,
            sorted(run_transaction_ids),
        ),
    )
    manifest = {
        "manifest_version": 1,
        "provider": provider,
        "export_run_id": run_id,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "files": manifest_files,
        "normalized_path": str(normalized_path.resolve()),
        "new_transactions": new_transactions,
        "existing_transactions": existing_transactions,
    }
    _write_manifest_once(manifest_dir / f"{run_id}.json", manifest)
    return {
        "new_transactions": new_transactions,
        "existing_transactions": existing_transactions,
    }


def _write_master_csv(connection, path: Path) -> None:
    ensure_private_directory(path.parent)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=NORMALIZED_COLUMNS,
            delimiter=";",
        )
        writer.writeheader()
        for row in transaction_rows(connection):
            writer.writerow(dict(row))
    os.replace(temporary, path)
    protect_file(path)


def _write_transactions_csv(path: Path, rows: Iterable) -> None:
    ensure_private_directory(path.parent)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=NORMALIZED_COLUMNS,
            delimiter=";",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))
    os.replace(temporary, path)
    protect_file(path)


def _archive_raw_file(source: Path, destination: Path, expected_hash: str) -> None:
    if destination.exists():
        current_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
        if current_hash != expected_hash:
            raise RuntimeError(f"Archivdatei hat unerwarteten Inhalt: {destination}")
        return
    shutil.copyfile(source, destination)
    protect_file(destination)


def _discover_runs(output_dir: Path) -> tuple[Path, ...]:
    if not output_dir.is_dir():
        return ()
    return tuple(
        path
        for path in output_dir.iterdir()
        if path.is_dir() and _is_run_id(path.name)
    )


def _accounts(config: AppConfig) -> dict[str, AccountDefinition]:
    configured = config.export.accounts
    if not configured and config.provider == "volksbank":
        configured = ALLOWED_ACCOUNTS
    accounts = {}
    for account in configured:
        accounts[account.filename] = AccountDefinition(
            provider=config.provider,
            name=account.name,
            number=account.iban,
            filename=account.filename,
        )
    if not accounts:
        raise ValueError(f"Keine Konten fuer {config.provider} konfiguriert.")
    return accounts


def _layout(store_root: Path) -> dict[str, Path]:
    root = store_root.expanduser().resolve()
    return {
        "root": root,
        "raw": root / "archive" / "raw",
        "manifests": root / "archive" / "manifests",
        "normalized_runs": root / "normalized" / "runs",
        "master_csv": root / "normalized" / "transactions.csv",
        "database": root / "database" / "transactions.sqlite3",
        "rules_database": root / "database" / "rules.sqlite3",
    }


def _empty_summary(store_root: Path) -> ImportSummary:
    layout = _layout(store_root)
    return ImportSummary(
        runs=0,
        source_files=0,
        parsed_rows=0,
        new_transactions=0,
        existing_transactions=0,
        total_transactions=0,
        database_path=layout["database"],
        normalized_path=layout["master_csv"],
    )


def _source_file_id(
    provider: str,
    run_id: str,
    filename: str,
    file_hash: str,
) -> str:
    value = (
        f"source-file-id-v1|{provider}|{run_id}|{filename}|{file_hash}"
    ).encode("utf-8")
    return "src_" + hashlib.sha256(value).hexdigest()


def _run_year_month(run_id: str) -> tuple[str, str]:
    if not _is_run_id(run_id):
        raise ValueError(f"Ungueltige Exportlauf-ID: {run_id}")
    return run_id[:4], run_id[4:6]


def _is_run_id(value: str) -> bool:
    import re

    return bool(re.fullmatch(r"\d{8}T\d{6}_\d{6}Z", value))


def _atomic_write_text(path: Path, content: str) -> None:
    ensure_private_directory(path.parent)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)
    protect_file(path)


def _write_manifest_once(path: Path, manifest: dict) -> None:
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        existing_hashes = {
            item["filename"]: item["sha256"] for item in existing["files"]
        }
        current_hashes = {
            item["filename"]: item["sha256"] for item in manifest["files"]
        }
        if (
            existing.get("provider") != manifest["provider"]
            or existing.get("export_run_id") != manifest["export_run_id"]
            or existing_hashes != current_hashes
        ):
            raise RuntimeError(f"Archivmanifest widerspricht Exportlauf: {path}")
        return
    _atomic_write_text(
        path,
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
