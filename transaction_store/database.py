from __future__ import annotations

import hashlib
import heapq
import json
import mimetypes
import os
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence
from uuid import uuid4

from banking_readonly.security import ensure_private_directory, protect_file

from .classification import SQL_CLASSIFICATION_STATUS_EXPRESSION
from .models import ParsedFile, ParsedTransaction


SCHEMA_VERSION = 13
BELEGE_DIRECTORY_ENV = "BSV_BELEGE_DIR"
VORGANG_STATUS_IN_PROGRESS = "in_bearbeitung"
VORGANG_STATUS_COMPLETED = "abgeschlossen"
DOCUMENT_CATEGORIES = (
    "rechnungen",
    "spendenbescheinigungen",
    "sonstige_dokumente",
)
TERMIN_STATUS_PLANNED = "geplant"
TERMIN_STATUS_COMPLETED = "abgeschlossen"
TERMIN_STATUS_CANCELLED = "abgesagt"
NORMALIZED_COLUMNS = (
    "transaktions_id",
    "datum",
    "kontoname",
    "kontonummer",
    "zahlungsbeteiligter",
    "verwendungszweck",
    "betrag",
    "kontostand_konto",
    "kontostand_gesamt",
    "kontostand_gesamt_vollstaendig",
    "transaktionstyp",
    "oberkategorie",
    "unterkategorie",
    "sphaere",
    "fachliche_beschreibung",
    "klassifikationsstatus",
    "budget_id",
)


def connect_database(path: Path) -> sqlite3.Connection:
    ensure_private_directory(path.parent)
    try:
        connection = _open_database(path)
    except sqlite3.OperationalError as exc:
        if not _is_sqlite_open_error(exc):
            raise
        _discard_empty_sqlite_sidecars(path)
        connection = _open_database(path)
    protect_file(path)
    return connection


def _open_database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        _initialize_schema(connection)
    except Exception:
        connection.close()
        raise
    return connection


def _is_sqlite_open_error(exc: sqlite3.OperationalError) -> bool:
    return "unable to open database file" in str(exc).casefold()


def _sqlite_sidecar_path(path: Path, suffix: str) -> Path:
    return path.with_name(f"{path.name}{suffix}")


def _discard_empty_sqlite_sidecars(path: Path) -> None:
    wal_path = _sqlite_sidecar_path(path, "-wal")
    shm_path = _sqlite_sidecar_path(path, "-shm")
    if not wal_path.exists() and not shm_path.exists():
        return
    wal_size = _safe_file_size(wal_path)
    if wal_size is None:
        raise sqlite3.OperationalError(
            "SQLite-Nebendatei kann nicht geprueft werden: "
            f"{wal_path}"
        )
    if wal_size > 0:
        raise sqlite3.OperationalError(
            "SQLite-WAL-Datei enthaelt noch Daten und wurde nicht automatisch "
            f"geloescht: {wal_path}"
        )
    for sidecar_path in (shm_path, wal_path):
        if not sidecar_path.exists():
            continue
        try:
            sidecar_path.unlink()
        except OSError as exc:
            raise sqlite3.OperationalError(
                "SQLite-Nebendatei kann nicht bereinigt werden: "
                f"{sidecar_path} ({exc})"
            ) from exc


def _safe_file_size(path: Path) -> int | None:
    if not path.exists():
        return 0
    try:
        return path.stat().st_size
    except OSError:
        return None


def configured_belege_directory(database_path: Path) -> Path:
    configured = str(os.getenv(BELEGE_DIRECTORY_ENV) or "").strip()
    directory = (
        Path(configured).expanduser()
        if configured
        else database_path.expanduser().resolve().parent / "belege"
    )
    resolved = directory.resolve()
    ensure_private_directory(resolved)
    return resolved


def sync_belege_directory(
    connection: sqlite3.Connection,
    directory: Path,
) -> int:
    resolved_directory = directory.expanduser().resolve()
    ensure_private_directory(resolved_directory)
    now = datetime.now(timezone.utc).isoformat()
    connection.execute(
        """
        UPDATE belege
        SET vorhanden = 0, aktualisiert_am = ?
        WHERE dateipfad = ?
           OR dateipfad LIKE ?
        """,
        (
            now,
            str(resolved_directory),
            str(resolved_directory) + os.sep + "%",
        ),
    )
    synchronized = 0
    for file_path in sorted(
        path
        for path in resolved_directory.rglob("*")
        if path.is_file()
    ):
        resolved_file = file_path.resolve()
        stat = resolved_file.stat()
        sha256 = _file_sha256(resolved_file)
        existing = connection.execute(
            "SELECT beleg_id FROM belege WHERE dateipfad = ?",
            (str(resolved_file),),
        ).fetchone()
        beleg_id = (
            str(existing["beleg_id"])
            if existing is not None
            else f"beleg_{uuid4().hex}"
        )
        connection.execute(
            """
            INSERT INTO belege (
                beleg_id, dateiname, dateipfad, dateityp,
                dateigroesse, datei_sha256, vorhanden, quelle,
                erstellt_am, aktualisiert_am
            ) VALUES (?, ?, ?, ?, ?, ?, 1, 'ordner_scan', ?, ?)
            ON CONFLICT(beleg_id) DO UPDATE SET
                dateiname = excluded.dateiname,
                dateipfad = excluded.dateipfad,
                dateityp = excluded.dateityp,
                dateigroesse = excluded.dateigroesse,
                datei_sha256 = excluded.datei_sha256,
                vorhanden = 1,
                aktualisiert_am = excluded.aktualisiert_am
            """,
            (
                beleg_id,
                resolved_file.name,
                str(resolved_file),
                mimetypes.guess_type(resolved_file.name)[0] or "",
                stat.st_size,
                sha256,
                now,
                now,
            ),
        )
        synchronized += 1
    return synchronized


def import_parsed_file(
    connection: sqlite3.Connection,
    parsed: ParsedFile,
    file_id: str,
    run_id: str,
    original_path: Path,
    archive_path: Path,
) -> tuple[int, int]:
    now = datetime.now(timezone.utc).isoformat()
    account_id = _account_id(parsed.account.provider, parsed.account.number)
    connection.execute(
        """
        INSERT INTO accounts (
            account_id, provider, account_name, account_number
        ) VALUES (?, ?, ?, ?)
        ON CONFLICT(account_id) DO UPDATE SET
            account_name = excluded.account_name
        """,
        (
            account_id,
            parsed.account.provider,
            parsed.account.name,
            parsed.account.number,
        ),
    )
    if parsed.account_balance is not None:
        connection.execute(
            """
            UPDATE accounts
            SET current_balance_minor = ?,
                balance_currency = ?,
                balance_as_of = ?,
                balance_run_id = ?
            WHERE account_id = ?
              AND (
                    current_balance_minor IS NULL
                    OR balance_as_of < ?
                    OR (
                        balance_as_of = ?
                        AND balance_run_id <= ?
                    )
              )
            """,
            (
                int(parsed.account_balance * 100),
                parsed.balance_currency or "",
                parsed.balance_as_of or "",
                run_id,
                account_id,
                parsed.balance_as_of or "",
                parsed.balance_as_of or "",
                run_id,
            ),
        )
    connection.execute(
        """
        INSERT INTO source_files (
            file_id, provider, export_run_id, original_filename,
            original_path, archive_path, file_sha256, encoding,
            delimiter, row_count, imported_at, account_balance_minor,
            balance_as_of
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file_id) DO UPDATE SET
            account_balance_minor = COALESCE(
                excluded.account_balance_minor,
                source_files.account_balance_minor
            ),
            balance_as_of = CASE
                WHEN excluded.balance_as_of <> ''
                THEN excluded.balance_as_of
                ELSE source_files.balance_as_of
            END
        """,
        (
            file_id,
            parsed.account.provider,
            run_id,
            parsed.path.name,
            str(original_path),
            str(archive_path),
            parsed.sha256,
            parsed.encoding,
            parsed.delimiter,
            len(parsed.transactions),
            now,
            (
                int(parsed.account_balance * 100)
                if parsed.account_balance is not None
                else None
            ),
            parsed.balance_as_of or "",
        ),
    )

    new_count = 0
    existing_count = 0
    for transaction in parsed.transactions:
        inserted = _insert_transaction(
            connection,
            transaction,
            account_id,
            now,
        )
        if inserted:
            new_count += 1
        else:
            existing_count += 1
        connection.execute(
            """
            INSERT INTO transaction_sources (
                transaction_id, file_id, source_row_number,
                account_balance_minor
            ) VALUES (?, ?, ?, ?)
            ON CONFLICT(
                transaction_id, file_id, source_row_number
            ) DO UPDATE SET
                account_balance_minor = COALESCE(
                    excluded.account_balance_minor,
                    transaction_sources.account_balance_minor
                )
            """,
            (
                transaction.transaction_id,
                file_id,
                transaction.source_row_number,
                (
                    int(transaction.account_balance * 100)
                    if transaction.account_balance is not None
                    else None
                ),
            ),
        )
    return new_count, existing_count


def transaction_rows(connection: sqlite3.Connection) -> Iterable[sqlite3.Row]:
    return connection.execute(
        """
        SELECT *
        FROM normalized_transactions
        ORDER BY datum, kontoname, transaktions_id
        """
    )


def transaction_rows_by_ids(
    connection: sqlite3.Connection,
    transaction_ids: Sequence[str],
) -> list[sqlite3.Row]:
    rows = []
    for offset in range(0, len(transaction_ids), 900):
        chunk = transaction_ids[offset : offset + 900]
        placeholders = ", ".join("?" for _ in chunk)
        rows.extend(
            connection.execute(
                f"""
                SELECT *
                FROM normalized_transactions
                WHERE transaktions_id IN ({placeholders})
                """,
                tuple(chunk),
            )
        )
    return sorted(
        rows,
        key=lambda row: (
            row["datum"],
            row["kontoname"],
            row["transaktions_id"],
        ),
    )


def transaction_count(connection: sqlite3.Connection) -> int:
    return int(connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0])


def recalculate_account_balances(
    connection: sqlite3.Connection,
    provider: str,
    account_number: str,
) -> int:
    account_id = _account_id(provider, account_number)
    account = connection.execute(
        """
        SELECT current_balance_minor, balance_as_of
        FROM accounts
        WHERE account_id = ?
        """,
        (account_id,),
    ).fetchone()
    if account is None or account["current_balance_minor"] is None:
        return 0

    transactions = connection.execute(
        """
        SELECT transaction_id, booking_date, amount_minor,
               account_balance_minor, source_info
        FROM transactions
        WHERE account_id = ?
        """,
        (account_id,),
    ).fetchall()
    if not transactions:
        return 0
    connection.execute(
        """
        UPDATE transactions
        SET account_balance_minor = NULL
        WHERE account_id = ?
          AND LOWER(source_info) LIKE '%vorgemerkt%'
        """,
        (account_id,),
    )
    transactions = [
        row
        for row in transactions
        if "vorgemerkt" not in row["source_info"].casefold()
    ]
    if not transactions:
        return 0

    balance_as_of = account["balance_as_of"]
    latest_booking_date = max(row["booking_date"] for row in transactions)
    if balance_as_of and latest_booking_date > balance_as_of:
        raise RuntimeError(
            "Kontostandsanker ist aelter als der neueste Umsatz fuer "
            f"{account_number[-4:]}."
        )

    ordered_ids = _ordered_transaction_ids(connection, account_id, transactions)
    by_id = {row["transaction_id"]: row for row in transactions}
    current_balance = int(account["current_balance_minor"])
    updated = 0
    for transaction_id in ordered_ids:
        transaction = by_id[transaction_id]
        existing_balance = transaction["account_balance_minor"]
        if existing_balance is not None and existing_balance != current_balance:
            if provider != "sparkasse":
                raise RuntimeError(
                    "Inkonsistenter rueckwaerts berechneter Kontostand fuer "
                    f"Transaktion {transaction_id}: "
                    f"{existing_balance / 100:.2f} statt "
                    f"{current_balance / 100:.2f}."
                )
        if existing_balance != current_balance:
            connection.execute(
                """
                UPDATE transactions
                SET account_balance_minor = ?
                WHERE transaction_id = ?
                """,
                (current_balance, transaction_id),
            )
            updated += 1
        current_balance -= int(transaction["amount_minor"])
    return updated


def _ordered_transaction_ids(
    connection: sqlite3.Connection,
    account_id: str,
    transactions: Sequence[sqlite3.Row],
) -> list[str]:
    ids_by_date: dict[str, list[str]] = defaultdict(list)
    date_by_id = {}
    for transaction in transactions:
        transaction_id = transaction["transaction_id"]
        booking_date = transaction["booking_date"]
        ids_by_date[booking_date].append(transaction_id)
        date_by_id[transaction_id] = booking_date

    source_rows = connection.execute(
        """
        SELECT ts.file_id, ts.source_row_number, ts.transaction_id
        FROM transaction_sources AS ts
        JOIN transactions AS t
          ON t.transaction_id = ts.transaction_id
        WHERE t.account_id = ?
        ORDER BY ts.file_id, ts.source_row_number
        """,
        (account_id,),
    ).fetchall()
    source_sequences: dict[str, list[str]] = defaultdict(list)
    for row in source_rows:
        source_sequences[row["file_id"]].append(row["transaction_id"])

    edges_by_date: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for sequence in source_sequences.values():
        previous_by_date = {}
        for transaction_id in sequence:
            if transaction_id not in date_by_id:
                continue
            booking_date = date_by_id[transaction_id]
            previous = previous_by_date.get(booking_date)
            if previous is not None and previous != transaction_id:
                edges_by_date[booking_date][previous].add(transaction_id)
            previous_by_date[booking_date] = transaction_id

    ordered = []
    for booking_date in sorted(ids_by_date, reverse=True):
        transaction_ids = ids_by_date[booking_date]
        indegree = {transaction_id: 0 for transaction_id in transaction_ids}
        for targets in edges_by_date[booking_date].values():
            for target in targets:
                indegree[target] += 1
        available = [
            transaction_id
            for transaction_id, degree in indegree.items()
            if degree == 0
        ]
        heapq.heapify(available)
        date_order = []
        while available:
            transaction_id = heapq.heappop(available)
            date_order.append(transaction_id)
            for target in sorted(
                edges_by_date[booking_date].get(transaction_id, ())
            ):
                indegree[target] -= 1
                if indegree[target] == 0:
                    heapq.heappush(available, target)
        if len(date_order) != len(transaction_ids):
            raise RuntimeError(
                "Widerspruechliche Umsatzreihenfolge am "
                f"{booking_date} fuer Konto {account_id[-8:]}."
            )
        ordered.extend(date_order)
    return ordered


def _insert_transaction(
    connection: sqlite3.Connection,
    transaction: ParsedTransaction,
    account_id: str,
    now: str,
) -> bool:
    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO transactions (
            transaction_id, fingerprint, occurrence, provider, account_id,
            account_name, account_number, booking_date, value_date,
            counterparty, amount, currency, booking_text, purpose,
            amount_minor, counterparty_account, creditor_id, mandate_reference,
            source_info, raw_fields_json, first_seen_at,
            account_balance_minor
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?
        )
        """,
        (
            transaction.transaction_id,
            transaction.fingerprint,
            transaction.occurrence,
            transaction.provider,
            account_id,
            transaction.account_name,
            transaction.account_number,
            transaction.booking_date,
            transaction.value_date,
            transaction.counterparty,
            format(transaction.amount, ".2f"),
            transaction.currency,
            transaction.booking_text,
            transaction.purpose,
            int(transaction.amount * 100),
            transaction.counterparty_account,
            transaction.creditor_id,
            transaction.mandate_reference,
            transaction.source_info,
            json.dumps(
                dict(transaction.raw_fields),
                ensure_ascii=False,
                sort_keys=True,
            ),
            now,
            (
                int(transaction.account_balance * 100)
                if transaction.account_balance is not None
                else None
            ),
        ),
    )
    inserted = cursor.rowcount == 1
    incoming_balance = (
        int(transaction.account_balance * 100)
        if transaction.account_balance is not None
        else None
    )
    if not inserted and incoming_balance is not None:
        existing_balance = connection.execute(
            """
            SELECT account_balance_minor
            FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction.transaction_id,),
        ).fetchone()[0]
        if existing_balance is None:
            connection.execute(
                """
                UPDATE transactions
                SET account_balance_minor = ?
                WHERE transaction_id = ?
                """,
                (incoming_balance, transaction.transaction_id),
            )
        elif (
            existing_balance != incoming_balance
            and transaction.provider == "sparkasse"
        ):
            connection.execute(
                """
                UPDATE transactions
                SET account_balance_minor = ?
                WHERE transaction_id = ?
                """,
                (incoming_balance, transaction.transaction_id),
            )
        elif existing_balance != incoming_balance:
            raise RuntimeError(
                "Inkonsistenter Kontostand fuer ueberlappende "
                f"Transaktion {transaction.transaction_id}: "
                f"{existing_balance / 100:.2f} statt "
                f"{incoming_balance / 100:.2f}."
            )
    return inserted


def _initialize_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_info (
            version INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            account_name TEXT NOT NULL,
            account_number TEXT NOT NULL,
            current_balance_minor INTEGER,
            balance_currency TEXT NOT NULL DEFAULT '',
            balance_as_of TEXT NOT NULL DEFAULT '',
            balance_run_id TEXT NOT NULL DEFAULT '',
            UNIQUE(provider, account_number)
        );

        CREATE TABLE IF NOT EXISTS source_files (
            file_id TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            export_run_id TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            original_path TEXT NOT NULL,
            archive_path TEXT NOT NULL,
            file_sha256 TEXT NOT NULL,
            encoding TEXT NOT NULL,
            delimiter TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            imported_at TEXT NOT NULL,
            account_balance_minor INTEGER,
            balance_as_of TEXT NOT NULL DEFAULT '',
            UNIQUE(provider, export_run_id, original_filename)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            fingerprint TEXT NOT NULL,
            occurrence INTEGER NOT NULL,
            provider TEXT NOT NULL,
            account_id TEXT NOT NULL REFERENCES accounts(account_id),
            account_name TEXT NOT NULL,
            account_number TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            value_date TEXT NOT NULL,
            counterparty TEXT NOT NULL,
            amount TEXT NOT NULL,
            currency TEXT NOT NULL,
            booking_text TEXT NOT NULL,
            purpose TEXT NOT NULL,
            amount_minor INTEGER NOT NULL,
            counterparty_account TEXT NOT NULL,
            creditor_id TEXT NOT NULL,
            mandate_reference TEXT NOT NULL,
            source_info TEXT NOT NULL,
            raw_fields_json TEXT NOT NULL,
            first_seen_at TEXT NOT NULL,
            transaction_type TEXT NOT NULL DEFAULT '',
            top_category TEXT NOT NULL DEFAULT '',
            sub_category TEXT NOT NULL DEFAULT '',
            sphere TEXT NOT NULL DEFAULT '',
            professional_description TEXT NOT NULL DEFAULT '',
            account_balance_minor INTEGER,
            UNIQUE(fingerprint, occurrence)
        );

        CREATE TABLE IF NOT EXISTS transaction_sources (
            transaction_id TEXT NOT NULL
                REFERENCES transactions(transaction_id),
            file_id TEXT NOT NULL REFERENCES source_files(file_id),
            source_row_number INTEGER NOT NULL,
            account_balance_minor INTEGER,
            PRIMARY KEY(transaction_id, file_id, source_row_number)
        );

        CREATE INDEX IF NOT EXISTS idx_transactions_date
            ON transactions(booking_date);
        CREATE INDEX IF NOT EXISTS idx_transactions_account
            ON transactions(account_number, booking_date);
        CREATE INDEX IF NOT EXISTS idx_transactions_counterparty
            ON transactions(counterparty);
        """
    )
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT version FROM schema_info LIMIT 1"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO schema_info(version) VALUES (?)",
                (SCHEMA_VERSION,),
            )
        else:
            version = int(row[0])
            migrations = {
                2: _migrate_v2_to_v3,
                3: _migrate_v3_to_v4,
                4: _migrate_v4_to_v5,
                5: _migrate_v5_to_v6,
                6: _migrate_v6_to_v7,
                7: _migrate_v7_to_v8,
                8: _migrate_v8_to_v9,
                9: _migrate_v9_to_v10,
                10: _migrate_v10_to_v11,
                11: _migrate_v11_to_v12,
                12: _migrate_v12_to_v13,
            }
            while version < SCHEMA_VERSION:
                migration = migrations.get(version)
                if migration is None:
                    raise RuntimeError(
                        f"Nicht unterstuetzte Datenbankversion: {row[0]}"
                    )
                migration(connection)
                version += 1
            if version != SCHEMA_VERSION:
                raise RuntimeError(
                    f"Nicht unterstuetzte Datenbankversion: {row[0]}"
                )
        _create_budgets_table(connection)
        _create_vorgaenge_table(connection)
        _create_transaction_link_tables(connection)
        _create_document_tables(connection)
        _create_termin_tables(connection)
        _create_vorgang_triggers(connection)
        _enforce_vorgang_completion_invariant(connection)
        _recreate_normalized_view(connection)
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def _migrate_v2_to_v3(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(transactions)")
    }
    definitions = {
        "transaction_type": "TEXT NOT NULL DEFAULT ''",
        "top_category": "TEXT NOT NULL DEFAULT ''",
        "sub_category": "TEXT NOT NULL DEFAULT ''",
        "sphere": "TEXT NOT NULL DEFAULT ''",
        "professional_description": "TEXT NOT NULL DEFAULT ''",
    }
    for name, definition in definitions.items():
        if name not in columns:
            connection.execute(
                f"ALTER TABLE transactions ADD COLUMN {name} {definition}"
            )
    connection.execute(
        "UPDATE schema_info SET version = 3",
    )


def _migrate_v3_to_v4(connection: sqlite3.Connection) -> None:
    _create_budgets_table(connection)
    connection.execute(
        "UPDATE schema_info SET version = 4",
    )


def _migrate_v4_to_v5(connection: sqlite3.Connection) -> None:
    _create_transaction_link_tables(connection)
    connection.execute(
        "UPDATE schema_info SET version = 5",
    )


def _migrate_v5_to_v6(connection: sqlite3.Connection) -> None:
    additions = {
        "accounts": {
            "current_balance_minor": "INTEGER",
            "balance_currency": "TEXT NOT NULL DEFAULT ''",
            "balance_as_of": "TEXT NOT NULL DEFAULT ''",
            "balance_run_id": "TEXT NOT NULL DEFAULT ''",
        },
        "source_files": {
            "account_balance_minor": "INTEGER",
            "balance_as_of": "TEXT NOT NULL DEFAULT ''",
        },
        "transactions": {
            "account_balance_minor": "INTEGER",
        },
        "transaction_sources": {
            "account_balance_minor": "INTEGER",
        },
    }
    for table, definitions in additions.items():
        columns = {
            row["name"]
            for row in connection.execute(f"PRAGMA table_info({table})")
        }
        for name, definition in definitions.items():
            if name not in columns:
                connection.execute(
                    f"ALTER TABLE {table} ADD COLUMN {name} {definition}"
                )
    connection.execute(
        "UPDATE schema_info SET version = 6",
    )


def _migrate_v6_to_v7(connection: sqlite3.Connection) -> None:
    _create_vorgaenge_table(connection)
    connection.execute(
        """
        INSERT OR IGNORE INTO vorgaenge (
            vorgangs_id, vorgangstyp, status
        )
        SELECT DISTINCT
            vorgangs_id, '', ?
        FROM transaktion_vorgaenge
        """,
        (VORGANG_STATUS_IN_PROGRESS,),
    )
    connection.execute(
        """
        CREATE TABLE transaktion_vorgaenge_v7 (
            transaktions_id TEXT NOT NULL
                REFERENCES transactions(transaction_id)
                ON DELETE CASCADE,
            vorgangs_id TEXT NOT NULL
                REFERENCES vorgaenge(vorgangs_id)
                ON DELETE CASCADE,
            PRIMARY KEY (transaktions_id, vorgangs_id)
        )
        """
    )
    connection.execute(
        """
        INSERT INTO transaktion_vorgaenge_v7 (
            transaktions_id, vorgangs_id
        )
        SELECT transaktions_id, vorgangs_id
        FROM transaktion_vorgaenge
        """
    )
    connection.execute("DROP TABLE transaktion_vorgaenge")
    connection.execute(
        "ALTER TABLE transaktion_vorgaenge_v7 RENAME TO transaktion_vorgaenge"
    )
    _backfill_transaction_vorgaenge(connection)
    connection.execute("UPDATE schema_info SET version = 7")


def _migrate_v7_to_v8(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TEMP TABLE pending_transactions_v8 AS
        SELECT transaction_id
        FROM transactions
        WHERE provider = 'sparkasse'
          AND LOWER(source_info) LIKE '%vorgemerkt%'
        """
    )
    connection.execute(
        """
        CREATE TEMP TABLE pending_vorgaenge_v8 AS
        SELECT tv.vorgangs_id
        FROM transaktion_vorgaenge AS tv
        JOIN pending_transactions_v8 AS pending
          ON pending.transaction_id = tv.transaktions_id
        WHERE tv.vorgangs_id = 'vorgang_' || pending.transaction_id
        """
    )
    connection.execute(
        """
        UPDATE source_files
        SET row_count = row_count - (
            SELECT COUNT(*)
            FROM transaction_sources AS ts
            JOIN pending_transactions_v8 AS pending
              ON pending.transaction_id = ts.transaction_id
            WHERE ts.file_id = source_files.file_id
        )
        WHERE EXISTS (
            SELECT 1
            FROM transaction_sources AS ts
            JOIN pending_transactions_v8 AS pending
              ON pending.transaction_id = ts.transaction_id
            WHERE ts.file_id = source_files.file_id
        )
        """
    )
    connection.execute(
        """
        DELETE FROM transaction_sources
        WHERE transaction_id IN (
            SELECT transaction_id
            FROM pending_transactions_v8
        )
        """
    )
    connection.execute(
        """
        DELETE FROM transactions
        WHERE transaction_id IN (
            SELECT transaction_id
            FROM pending_transactions_v8
        )
        """
    )
    connection.execute(
        """
        DELETE FROM vorgaenge
        WHERE vorgangs_id IN (
            SELECT vorgangs_id
            FROM pending_vorgaenge_v8
        )
          AND NOT EXISTS (
                SELECT 1
                FROM transaktion_vorgaenge AS tv
                WHERE tv.vorgangs_id = vorgaenge.vorgangs_id
          )
        """
    )
    connection.execute("DROP TABLE pending_vorgaenge_v8")
    connection.execute("DROP TABLE pending_transactions_v8")
    connection.execute("UPDATE schema_info SET version = 8")


def _migrate_v8_to_v9(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(vorgaenge)")
    }
    if "status_manuell" not in columns:
        connection.execute(
            """
            ALTER TABLE vorgaenge
            ADD COLUMN status_manuell INTEGER NOT NULL DEFAULT 0
                CHECK (status_manuell IN (0, 1))
            """
        )
    connection.execute("UPDATE schema_info SET version = 9")


def _migrate_v9_to_v10(connection: sqlite3.Connection) -> None:
    connection.execute("UPDATE schema_info SET version = 10")


def _migrate_v10_to_v11(connection: sqlite3.Connection) -> None:
    _create_document_tables(connection)
    if _table_exists(connection, "transaktion_belege"):
        document_directory = configured_belege_directory(
            _database_path(connection)
        )
        now = datetime.now(timezone.utc).isoformat()
        legacy_ids = [
            str(row["beleg_id"])
            for row in connection.execute(
                """
                SELECT DISTINCT beleg_id
                FROM transaktion_belege
                ORDER BY beleg_id
                """
            )
        ]
        for beleg_id in legacy_ids:
            filename = _legacy_beleg_filename(beleg_id)
            file_path = (document_directory / filename).resolve()
            connection.execute(
                """
                INSERT OR IGNORE INTO belege (
                    beleg_id, dateiname, dateipfad, dateityp,
                    dateigroesse, datei_sha256, vorhanden, quelle,
                    erstellt_am, aktualisiert_am
                ) VALUES (?, ?, ?, '', NULL, '', ?, 'migration', ?, ?)
                """,
                (
                    beleg_id,
                    filename,
                    str(file_path),
                    int(file_path.is_file()),
                    now,
                    now,
                ),
            )
        connection.execute(
            """
            INSERT OR IGNORE INTO vorgang_belege (
                vorgangs_id, beleg_id, erstellt_am
            )
            SELECT
                tv.vorgangs_id,
                tb.beleg_id,
                ?
            FROM transaktion_belege AS tb
            JOIN transaktion_vorgaenge AS tv
              ON tv.transaktions_id = tb.transaktions_id
            """,
            (now,),
        )
        connection.execute("DROP TABLE transaktion_belege")
    connection.execute("UPDATE schema_info SET version = 11")


def _migrate_v11_to_v12(connection: sqlite3.Connection) -> None:
    _create_vorgaenge_table(connection)
    _create_document_tables(connection)
    _create_termin_tables(connection)
    connection.execute("UPDATE schema_info SET version = 12")


def _migrate_v12_to_v13(connection: sqlite3.Connection) -> None:
    _create_vorgaenge_table(connection)
    _create_transaction_link_tables(connection)
    _create_document_tables(connection)
    _create_termin_tables(connection)
    connection.execute(
        f"""
        CREATE TEMP TABLE auto_open_vorgaenge_v13 AS
        SELECT DISTINCT v.vorgangs_id
        FROM vorgaenge AS v
        JOIN transaktion_vorgaenge AS tv
          ON tv.vorgangs_id = v.vorgangs_id
        JOIN transactions AS t
          ON t.transaction_id = tv.transaktions_id
        WHERE v.vorgangs_id = 'vorgang_' || t.transaction_id
          AND v.status_manuell = 0
          AND v.status = '{VORGANG_STATUS_IN_PROGRESS}'
          AND TRIM(COALESCE(v.titel, '')) = ''
          AND TRIM(COALESCE(v.beschreibung, '')) = ''
        """
    )
    connection.execute(
        """
        DELETE FROM transaktion_vorgaenge
        WHERE vorgangs_id IN (
            SELECT vorgangs_id FROM auto_open_vorgaenge_v13
        )
        """
    )
    connection.execute(
        """
        DELETE FROM vorgaenge
        WHERE vorgangs_id IN (
            SELECT vorgangs_id FROM auto_open_vorgaenge_v13
        )
          AND NOT EXISTS (
                SELECT 1
                FROM transaktion_vorgaenge AS tv
                WHERE tv.vorgangs_id = vorgaenge.vorgangs_id
          )
        """
    )
    connection.execute("DROP TABLE auto_open_vorgaenge_v13")
    connection.execute("UPDATE schema_info SET version = 13")


def _create_budgets_table(connection: sqlite3.Connection) -> None:
    budget_id_expression = _budget_id_expression(
        "saison",
        "oberkategorie",
        "unterkategorie",
    )
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS budgets (
            saison TEXT NOT NULL
                CHECK (
                    LENGTH(saison) = 9
                    AND SUBSTR(saison, 5, 1) = '/'
                    AND CAST(SUBSTR(saison, 6, 4) AS INTEGER)
                        = CAST(SUBSTR(saison, 1, 4) AS INTEGER) + 1
                ),
            oberkategorie TEXT NOT NULL
                CHECK (TRIM(oberkategorie) <> ''),
            unterkategorie TEXT NOT NULL
                CHECK (TRIM(unterkategorie) <> ''),
            einnahmen NUMERIC NOT NULL DEFAULT 0,
            ausgaben NUMERIC NOT NULL DEFAULT 0,
            budget NUMERIC GENERATED ALWAYS AS (
                ausgaben - einnahmen
            ) STORED,
            budget_id TEXT GENERATED ALWAYS AS (
                {budget_id_expression}
            ) STORED,
            UNIQUE (budget_id)
        )
        """
    )


def _create_vorgaenge_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS vorgaenge (
            vorgangs_id TEXT PRIMARY KEY
                CHECK (TRIM(vorgangs_id) <> ''),
            titel TEXT NOT NULL DEFAULT '',
            beschreibung TEXT NOT NULL DEFAULT '',
            vorgangstyp TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT '{VORGANG_STATUS_IN_PROGRESS}'
                CHECK (
                    status IN (
                        '{VORGANG_STATUS_IN_PROGRESS}',
                        '{VORGANG_STATUS_COMPLETED}'
                    )
                ),
            status_manuell INTEGER NOT NULL DEFAULT 0
                CHECK (status_manuell IN (0, 1)),
            erstellt_am TEXT NOT NULL DEFAULT (
                STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now')
            ),
            aktualisiert_am TEXT NOT NULL DEFAULT (
                STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now')
            )
        )
        """
    )
    _add_columns_if_missing(
        connection,
        "vorgaenge",
        {
            "titel": "TEXT NOT NULL DEFAULT ''",
            "beschreibung": "TEXT NOT NULL DEFAULT ''",
        },
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_vorgaenge_status_typ
            ON vorgaenge(status, vorgangstyp)
        """
    )


def _create_transaction_link_tables(connection: sqlite3.Connection) -> None:
    _create_vorgaenge_table(connection)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS transaktion_vorgaenge (
            transaktions_id TEXT NOT NULL
                REFERENCES transactions(transaction_id)
                ON DELETE CASCADE,
            vorgangs_id TEXT NOT NULL
                REFERENCES vorgaenge(vorgangs_id)
                ON DELETE CASCADE,
            PRIMARY KEY (transaktions_id, vorgangs_id)
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transaktion_vorgaenge_vorgangs_id
            ON transaktion_vorgaenge(vorgangs_id)
        """
    )


def _create_document_tables(connection: sqlite3.Connection) -> None:
    categories = ", ".join(f"'{category}'" for category in DOCUMENT_CATEGORIES)
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS belege (
            beleg_id TEXT PRIMARY KEY
                CHECK (TRIM(beleg_id) <> ''),
            dateiname TEXT NOT NULL
                CHECK (TRIM(dateiname) <> ''),
            dateipfad TEXT NOT NULL UNIQUE
                CHECK (TRIM(dateipfad) <> ''),
            dateityp TEXT NOT NULL DEFAULT '',
            dateigroesse INTEGER
                CHECK (dateigroesse IS NULL OR dateigroesse >= 0),
            datei_sha256 TEXT NOT NULL DEFAULT '',
            vorhanden INTEGER NOT NULL DEFAULT 1
                CHECK (vorhanden IN (0, 1)),
            kategorie TEXT NOT NULL DEFAULT 'sonstige_dokumente'
                CHECK (kategorie IN ({categories})),
            dokumentdatum TEXT NOT NULL DEFAULT '',
            betrag TEXT NOT NULL DEFAULT '',
            aussteller TEXT NOT NULL DEFAULT '',
            empfaenger TEXT NOT NULL DEFAULT '',
            beschreibung TEXT NOT NULL DEFAULT '',
            quelle TEXT NOT NULL DEFAULT 'ordner_scan'
                CHECK (
                    quelle IN (
                        'ordner_scan',
                        'migration',
                        'manual',
                        'automatic'
                    )
                ),
            erstellt_am TEXT NOT NULL,
            aktualisiert_am TEXT NOT NULL
        )
        """
    )
    _add_columns_if_missing(
        connection,
        "belege",
        {
            "kategorie": "TEXT NOT NULL DEFAULT 'sonstige_dokumente'",
            "dokumentdatum": "TEXT NOT NULL DEFAULT ''",
            "betrag": "TEXT NOT NULL DEFAULT ''",
            "aussteller": "TEXT NOT NULL DEFAULT ''",
            "empfaenger": "TEXT NOT NULL DEFAULT ''",
            "beschreibung": "TEXT NOT NULL DEFAULT ''",
        },
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_belege_dateiname
            ON belege(dateiname)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_belege_sha256
            ON belege(datei_sha256)
            WHERE datei_sha256 <> ''
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS vorgang_belege (
            vorgangs_id TEXT NOT NULL
                REFERENCES vorgaenge(vorgangs_id)
                ON DELETE CASCADE,
            beleg_id TEXT NOT NULL
                REFERENCES belege(beleg_id)
                ON DELETE CASCADE,
            erstellt_am TEXT NOT NULL,
            PRIMARY KEY (vorgangs_id, beleg_id)
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_vorgang_belege_beleg_id
            ON vorgang_belege(beleg_id)
        """
    )


def _create_termin_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS termine (
            termin_id TEXT PRIMARY KEY
                CHECK (TRIM(termin_id) <> ''),
            titel TEXT NOT NULL
                CHECK (TRIM(titel) <> ''),
            beschreibung TEXT NOT NULL DEFAULT '',
            beginnt_am TEXT NOT NULL
                CHECK (TRIM(beginnt_am) <> ''),
            endet_am TEXT NOT NULL DEFAULT '',
            ort TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT '{TERMIN_STATUS_PLANNED}'
                CHECK (
                    status IN (
                        '{TERMIN_STATUS_PLANNED}',
                        '{TERMIN_STATUS_COMPLETED}',
                        '{TERMIN_STATUS_CANCELLED}'
                    )
                ),
            quelle TEXT NOT NULL DEFAULT 'manual'
                CHECK (quelle IN ('manual', 'automatic')),
            quellreferenz TEXT NOT NULL DEFAULT '',
            erstellt_am TEXT NOT NULL,
            aktualisiert_am TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_termine_status_begin
            ON termine(status, beginnt_am)
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS vorgang_termine (
            vorgangs_id TEXT NOT NULL
                REFERENCES vorgaenge(vorgangs_id)
                ON DELETE CASCADE,
            termin_id TEXT NOT NULL
                REFERENCES termine(termin_id)
                ON DELETE CASCADE,
            erstellt_am TEXT NOT NULL,
            PRIMARY KEY (vorgangs_id, termin_id)
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_vorgang_termine_termin_id
            ON vorgang_termine(termin_id)
        """
    )


def _backfill_transaction_vorgaenge(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        INSERT OR IGNORE INTO vorgaenge (
            vorgangs_id, vorgangstyp, status, erstellt_am, aktualisiert_am
        )
        SELECT
            'vorgang_' || transaction_id,
            transaction_type,
            '{VORGANG_STATUS_IN_PROGRESS}',
            first_seen_at,
            first_seen_at
        FROM transactions
        """
    )
    connection.execute(
        """
        UPDATE vorgaenge
        SET
            vorgangstyp = (
                SELECT transaction_type
                FROM transactions
                WHERE 'vorgang_' || transaction_id = vorgaenge.vorgangs_id
            ),
            aktualisiert_am = STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now')
        WHERE EXISTS (
            SELECT 1
            FROM transactions
            WHERE 'vorgang_' || transaction_id = vorgaenge.vorgangs_id
              AND transaction_type <> vorgaenge.vorgangstyp
        )
        """
    )
    connection.execute(
        """
        INSERT OR IGNORE INTO transaktion_vorgaenge (
            transaktions_id, vorgangs_id
        )
        SELECT transaction_id, 'vorgang_' || transaction_id
        FROM transactions
        """
    )


def _create_vorgang_triggers(connection: sqlite3.Connection) -> None:
    connection.execute("DROP TRIGGER IF EXISTS trg_transactions_create_vorgang")
    connection.execute("DROP TRIGGER IF EXISTS trg_transactions_update_vorgang")
    connection.execute(
        "DROP TRIGGER IF EXISTS "
        "trg_transaktion_vorgaenge_enforce_completion"
    )
    connection.execute(
        f"""
        CREATE TRIGGER trg_transactions_update_vorgang
        AFTER UPDATE OF
            transaction_type,
            top_category,
            sub_category,
            sphere,
            professional_description
        ON transactions
        BEGIN
            UPDATE vorgaenge
            SET
                aktualisiert_am = STRFTIME(
                    '%Y-%m-%dT%H:%M:%fZ',
                    'now'
                )
            WHERE vorgangs_id IN (
                SELECT tv.vorgangs_id
                FROM transaktion_vorgaenge AS tv
                WHERE tv.transaktions_id = NEW.transaction_id
            );

            UPDATE vorgaenge
            SET
                status = '{VORGANG_STATUS_IN_PROGRESS}',
                aktualisiert_am = STRFTIME(
                    '%Y-%m-%dT%H:%M:%fZ',
                    'now'
                )
            WHERE status = '{VORGANG_STATUS_COMPLETED}'
              AND vorgangs_id IN (
                    SELECT tv.vorgangs_id
                    FROM transaktion_vorgaenge AS tv
                    WHERE tv.transaktions_id = NEW.transaction_id
              )
              AND EXISTS (
                    SELECT 1
                    FROM transaktion_vorgaenge AS linked
                    JOIN transactions AS linked_transaction
                      ON linked_transaction.transaction_id =
                         linked.transaktions_id
                    WHERE linked.vorgangs_id = vorgaenge.vorgangs_id
                      AND (
                            TRIM(COALESCE(
                                linked_transaction.transaction_type,
                                ''
                            )) = ''
                            OR TRIM(COALESCE(
                                linked_transaction.top_category,
                                ''
                            )) = ''
                            OR TRIM(COALESCE(
                                linked_transaction.sub_category,
                                ''
                            )) = ''
                            OR TRIM(COALESCE(
                                linked_transaction.sphere,
                                ''
                            )) = ''
                      )
              );
        END
        """
    )
    connection.execute(
        f"""
        CREATE TRIGGER trg_transaktion_vorgaenge_enforce_completion
        AFTER INSERT ON transaktion_vorgaenge
        BEGIN
            UPDATE vorgaenge
            SET
                status = '{VORGANG_STATUS_IN_PROGRESS}',
                aktualisiert_am = STRFTIME(
                    '%Y-%m-%dT%H:%M:%fZ',
                    'now'
                )
            WHERE vorgangs_id = NEW.vorgangs_id
              AND status = '{VORGANG_STATUS_COMPLETED}'
              AND EXISTS (
                    SELECT 1
                    FROM transactions
                    WHERE transaction_id = NEW.transaktions_id
                      AND (
                            TRIM(COALESCE(transaction_type, '')) = ''
                            OR TRIM(COALESCE(top_category, '')) = ''
                            OR TRIM(COALESCE(sub_category, '')) = ''
                            OR TRIM(COALESCE(sphere, '')) = ''
                      )
              );
        END
        """
    )


def _enforce_vorgang_completion_invariant(
    connection: sqlite3.Connection,
) -> None:
    connection.execute(
        f"""
        UPDATE vorgaenge
        SET
            status = '{VORGANG_STATUS_IN_PROGRESS}',
            aktualisiert_am = STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now')
        WHERE status = '{VORGANG_STATUS_COMPLETED}'
          AND EXISTS (
                SELECT 1
                FROM transaktion_vorgaenge AS tv
                JOIN transactions AS linked_transaction
                  ON linked_transaction.transaction_id = tv.transaktions_id
                WHERE tv.vorgangs_id = vorgaenge.vorgangs_id
                  AND (
                        TRIM(COALESCE(
                            linked_transaction.transaction_type,
                            ''
                        )) = ''
                        OR TRIM(COALESCE(
                            linked_transaction.top_category,
                            ''
                        )) = ''
                        OR TRIM(COALESCE(
                            linked_transaction.sub_category,
                            ''
                        )) = ''
                        OR TRIM(COALESCE(
                            linked_transaction.sphere,
                            ''
                        )) = ''
                  )
          )
        """
    )


def _vorgang_status_expression(_column_prefix: str) -> str:
    return f"'{VORGANG_STATUS_IN_PROGRESS}'"


def _add_columns_if_missing(
    connection: sqlite3.Connection,
    table: str,
    definitions: dict[str, str],
) -> None:
    columns = {
        row["name"] for row in connection.execute(f"PRAGMA table_info({table})")
    }
    for name, definition in definitions.items():
        if name not in columns:
            connection.execute(
                f"ALTER TABLE {table} ADD COLUMN {name} {definition}"
            )


def _recreate_normalized_view(connection: sqlite3.Connection) -> None:
    season_expression = _season_expression("booking_date")
    budget_id_expression = _budget_id_expression(
        season_expression,
        "top_category",
        "sub_category",
    )
    total_balance_expression = """
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM accounts
                WHERE current_balance_minor IS NOT NULL
            )
            THEN PRINTF(
                '%.2f',
                (
                    SELECT SUM(current_balance_minor)
                    FROM accounts
                    WHERE current_balance_minor IS NOT NULL
                ) / 100.0
            )
            ELSE ''
        END
    """.strip()
    total_balance_complete_expression = """
        CASE
            WHEN (SELECT COUNT(*) FROM accounts) > 0
                AND (
                    SELECT COUNT(*)
                    FROM accounts
                    WHERE current_balance_minor IS NOT NULL
                ) = (SELECT COUNT(*) FROM accounts)
            THEN 1
            ELSE 0
        END
    """.strip()
    connection.execute("DROP VIEW IF EXISTS normalized_transactions")
    connection.execute(
        f"""
        CREATE VIEW normalized_transactions AS
        SELECT
            transaction_id AS transaktions_id,
            booking_date AS datum,
            account_name AS kontoname,
            account_number AS kontonummer,
            counterparty AS zahlungsbeteiligter,
            purpose AS verwendungszweck,
            amount AS betrag,
            CASE
                WHEN account_balance_minor IS NULL THEN ''
                ELSE PRINTF('%.2f', account_balance_minor / 100.0)
            END AS kontostand_konto,
            {total_balance_expression} AS kontostand_gesamt,
            {total_balance_complete_expression}
                AS kontostand_gesamt_vollstaendig,
            transaction_type AS transaktionstyp,
            top_category AS oberkategorie,
            sub_category AS unterkategorie,
            sphere AS sphaere,
            professional_description AS fachliche_beschreibung,
            {SQL_CLASSIFICATION_STATUS_EXPRESSION} AS klassifikationsstatus,
            CASE
                WHEN TRIM(COALESCE(top_category, '')) <> ''
                    AND TRIM(COALESCE(sub_category, '')) <> ''
                THEN {budget_id_expression}
                ELSE ''
            END AS budget_id
        FROM transactions
        """
    )


def _season_expression(date_column: str) -> str:
    year = f"CAST(SUBSTR({date_column}, 1, 4) AS INTEGER)"
    return f"""
        CASE
            WHEN CAST(SUBSTR({date_column}, 6, 2) AS INTEGER) >= 7
            THEN PRINTF('%04d/%04d', {year}, {year} + 1)
            ELSE PRINTF('%04d/%04d', {year} - 1, {year})
        END
    """.strip()


def _budget_id_expression(
    season_expression: str,
    top_category_expression: str,
    sub_category_expression: str,
) -> str:
    return f"""
        'budget_v1_'
        || REPLACE(({season_expression}), '/', '_')
        || '_'
        || LOWER(HEX(TRIM({top_category_expression})))
        || '_'
        || LOWER(HEX(TRIM({sub_category_expression})))
    """.strip()


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    return connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone() is not None


def _database_path(connection: sqlite3.Connection) -> Path:
    row = connection.execute("PRAGMA database_list").fetchone()
    if row is None or not str(row["file"] or "").strip():
        raise RuntimeError("Datenbankpfad konnte nicht ermittelt werden.")
    return Path(str(row["file"])).resolve()


def _legacy_beleg_filename(beleg_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", beleg_id).strip("._")
    if not cleaned:
        cleaned = "beleg"
    if cleaned != beleg_id:
        suffix = hashlib.sha256(beleg_id.encode("utf-8")).hexdigest()[:10]
        cleaned = f"{cleaned}_{suffix}"
    return cleaned[:180]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as document:
        for chunk in iter(lambda: document.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _account_id(provider: str, account_number: str) -> str:
    value = f"account-id-v1|{provider}|{account_number}".encode("utf-8")
    return "acct_" + hashlib.sha256(value).hexdigest()
