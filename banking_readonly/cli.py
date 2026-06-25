from __future__ import annotations

import argparse
import logging
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Optional, Sequence

from dotenv import load_dotenv

from .config import ConfigError, load_config
from .credentials import CredentialError, load_credentials
from .exporter import run_csv_export
from .logging_setup import configure_logging
from .runner import DependencyError, run_login_test
from banking_dashboard import run_dashboard
from banking_dashboard.player_payments import (
    clear_player_payment_session,
    run_player_payment_review,
    save_manual_player_payment,
)
from banking_dashboard.player_premiums import run_player_premium_report
from transaction_store import (
    import_existing_exports,
    import_transaction_directory,
    ingest_export_run,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = PROJECT_ROOT / "config.toml"
EXAMPLE_CONFIG = PROJECT_ROOT / "config.example.toml"
SPARKASSE_EXAMPLE_CONFIG = PROJECT_ROOT / "config.sparkasse.example.toml"
DEFAULT_TRANSACTION_ROOT = PROJECT_ROOT / "data" / "transactions"
DEFAULT_ENV_FILE = Path(r"D:\.secrets\bsv_banking.env")
DEFAULT_SOURCE_CONFIGS = (
    PROJECT_ROOT / "config.toml",
    PROJECT_ROOT / "config.sparkasse.local.toml",
)


def main(argv: Optional[Sequence[str]] = None) -> int:
    load_dotenv(DEFAULT_ENV_FILE, override=False)
    parser = _build_parser()
    args = parser.parse_args(argv)
    config_path = Path(args.config).expanduser()

    if args.init_config:
        return _initialize_config(config_path, EXAMPLE_CONFIG)
    if args.init_sparkasse_config:
        return _initialize_config(config_path, SPARKASSE_EXAMPLE_CONFIG)
    if args.import_transactions:
        return _import_transactions(args)
    if args.import_directory:
        return _import_transaction_directory(args)
    if args.dashboard:
        return _run_dashboard(args)

    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Konfigurationsfehler: {exc}", file=sys.stderr)
        return 2

    if args.validate_config:
        try:
            if config.credentials.mode == "env":
                credentials = load_credentials(config.credentials)
                del credentials
        except CredentialError as exc:
            print(f"Credential-Fehler: {exc}", file=sys.stderr)
            return 2
        print("Konfiguration und Credential-Quelle sind gueltig.")
        return 0

    logger, log_path = configure_logging(config.runtime.log_dir)
    operation = "CSV-Export" if args.export_csv else "Onlinebanking-Login-Test"
    logger.info("%s gestartet. Logdatei: %s", operation, log_path)

    try:
        if args.export_csv:
            paths = run_csv_export(config, logger)
            summary = ingest_export_run(
                config,
                paths,
                Path(args.transaction_root),
            )
            print(
                f"\nCSV-Export abgeschlossen: {paths[0].parent}\n"
                f"Transaktionsdatenbank: {summary.database_path}\n"
                f"Gesamtbestand: {summary.total_transactions} Transaktionen\n"
            )
        else:
            run_login_test(config, logger)
    except KeyboardInterrupt:
        logger.warning("Test durch Benutzer abgebrochen.")
        return 130
    except DependencyError as exc:
        logger.error("%s", exc)
        return 3
    except Exception as exc:
        logger.exception("%s fehlgeschlagen: %s", operation, exc)
        return 1

    logger.info("%s erfolgreich beendet.", operation)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Onlinebanking-Export mit manueller MFA, sicherer Abmeldung und "
            "lokalem Transaktionsarchiv."
        )
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Pfad zur lokalen TOML-Konfiguration (Standard: config.toml)",
    )
    parser.add_argument(
        "--init-config",
        action="store_true",
        help="Volksbank-Vorlage einmalig als lokale Konfiguration kopieren",
    )
    parser.add_argument(
        "--init-sparkasse-config",
        action="store_true",
        help="Sparkassen-Vorlage einmalig als lokale Konfiguration kopieren",
    )
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Konfiguration pruefen, ohne einen Browser zu starten",
    )
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help=(
            "CSV-Umsaetze der fest freigegebenen Konten im bankspezifisch "
            "zugelassenen Format herunterladen"
        ),
    )
    parser.add_argument(
        "--import-transactions",
        action="store_true",
        help=(
            "Vorhandene Volksbank- und Sparkassenexporte archivieren, "
            "normalisieren und in die Transaktionsdatenbank importieren"
        ),
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Lokales Finanzdashboard starten",
    )
    parser.add_argument(
        "--import-directory",
        help=(
            "Verzeichnis rekursiv nach unterstuetzten historischen "
            "Transaktionsauszuegen durchsuchen und importieren"
        ),
    )
    parser.add_argument(
        "--dashboard-host",
        default="127.0.0.1",
        help="Bind-Adresse des Dashboards (Standard: 127.0.0.1)",
    )
    parser.add_argument(
        "--dashboard-port",
        type=int,
        default=8765,
        help="Port des Dashboards (Standard: 8765)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Dashboard starten, ohne den Browser automatisch zu oeffnen",
    )
    parser.add_argument(
        "--source-config",
        action="append",
        default=[],
        help=(
            "Bankkonfiguration fuer --import-transactions; kann mehrfach "
            "angegeben werden"
        ),
    )
    parser.add_argument(
        "--transaction-root",
        default=str(DEFAULT_TRANSACTION_ROOT),
        help="Wurzelverzeichnis fuer Archiv, Normaldateien und SQLite-Datenbank",
    )
    return parser


def _initialize_config(config_path: Path, template_path: Path) -> int:
    destination = config_path.resolve()
    if destination.exists():
        print(
            f"Konfiguration existiert bereits und wird nicht ueberschrieben: "
            f"{destination}",
            file=sys.stderr,
        )
        return 2
    if not template_path.is_file():
        print(f"Konfigurationsvorlage fehlt: {template_path}", file=sys.stderr)
        return 2

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template_path, destination)
    print(f"Konfiguration angelegt: {destination}")
    print("Jetzt Credential-Quelle und Konten-Allowlist pruefen.")
    return 0


def _import_transactions(args: argparse.Namespace) -> int:
    config_paths = _source_config_paths(args)
    if not config_paths:
        print(
            "Keine Bankkonfiguration fuer den Transaktionsimport gefunden.",
            file=sys.stderr,
        )
        return 2

    try:
        configs = [load_config(path) for path in config_paths]
        summary = import_existing_exports(
            configs,
            Path(args.transaction_root),
        )
    except (ConfigError, OSError, ValueError, RuntimeError) as exc:
        print(f"Transaktionsimport fehlgeschlagen: {exc}", file=sys.stderr)
        return 1

    print(
        "Transaktionsimport abgeschlossen.\n"
        f"Exportlaeufe: {summary.runs}\n"
        f"Quelldateien: {summary.source_files}\n"
        f"Gelesene Zeilen: {summary.parsed_rows}\n"
        f"Neue Transaktionen: {summary.new_transactions}\n"
        f"Bereits vorhanden: {summary.existing_transactions}\n"
        f"Gesamtbestand: {summary.total_transactions}\n"
        f"Datenbank: {summary.database_path}\n"
        f"Normalisierte CSV: {summary.normalized_path}"
    )
    return 0


def _import_transaction_directory(args: argparse.Namespace) -> int:
    config_paths = _source_config_paths(args)
    if not config_paths:
        print(
            "Keine Bankkonfiguration fuer den Verzeichnisimport gefunden.",
            file=sys.stderr,
        )
        return 2

    try:
        configs = [load_config(path) for path in config_paths]
        summary = import_transaction_directory(
            configs,
            Path(args.import_directory),
            Path(args.transaction_root),
        )
    except (ConfigError, OSError, ValueError, RuntimeError) as exc:
        print(f"Verzeichnisimport fehlgeschlagen: {exc}", file=sys.stderr)
        return 1

    result = summary.import_summary
    print(
        "Historischer Verzeichnisimport abgeschlossen.\n"
        f"Erkannte Auszuege: {summary.recognized_files}\n"
        f"Ignorierte CSV-Dateien: {summary.ignored_files}\n"
        f"Gelesene Zeilen: {result.parsed_rows}\n"
        f"Neue Transaktionen: {result.new_transactions}\n"
        f"Bereits vorhanden: {result.existing_transactions}\n"
        f"Gesamtbestand: {result.total_transactions}"
    )
    for account in summary.accounts:
        print(
            f"- {account.account_name}: {account.date_from or 'keine Buchung'}"
            f" bis {account.date_to or 'keine Buchung'}, "
            f"{account.unique_transactions} eindeutige Transaktionen, "
            f"{account.overlapping_transactions} Ueberlappungen"
        )
    print(f"Datenbank: {result.database_path}")
    print(f"Normalisierte CSV: {result.normalized_path}")
    return 0


def _source_config_paths(args: argparse.Namespace) -> list[Path]:
    return (
        [Path(value).expanduser() for value in args.source_config]
        if args.source_config
        else [path for path in DEFAULT_SOURCE_CONFIGS if path.is_file()]
    )


def _run_dashboard(args: argparse.Namespace) -> int:
    transaction_root = Path(args.transaction_root)
    database_path = (
        transaction_root
        / "database"
        / "transactions.sqlite3"
    )
    config_paths = _source_config_paths(args)
    refresh_action = (
        _dashboard_refresh_action(config_paths, transaction_root)
        if config_paths
        else None
    )
    clear_player_payment_session()
    try:
        run_dashboard(
            database_path=database_path,
            host=args.dashboard_host,
            port=args.dashboard_port,
            open_browser=not args.no_browser,
            rules_database_path=database_path.parent / "rules.sqlite3",
            refresh_action=refresh_action,
            player_premium_action=run_player_premium_report,
            player_payment_action=run_player_payment_review,
            player_payment_update_action=save_manual_player_payment,
        )
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f"Dashboard konnte nicht gestartet werden: {exc}", file=sys.stderr)
        return 1
    finally:
        clear_player_payment_session()
    return 0


def _dashboard_refresh_action(
    config_paths: Sequence[Path],
    transaction_root: Path,
):
    def refresh() -> dict[str, object]:
        totals = {
            "providers": [],
            "new_transactions": 0,
            "existing_transactions": 0,
            "total_transactions": 0,
        }
        for config_path in config_paths:
            config = load_config(config_path)
            logger, _ = configure_logging(config.runtime.log_dir)
            paths = run_csv_export(config, logger)
            summary = ingest_export_run(config, paths, transaction_root)
            totals["providers"].append(config.provider)
            totals["new_transactions"] += summary.new_transactions
            totals["existing_transactions"] += summary.existing_transactions
            totals["total_transactions"] = summary.total_transactions
        return totals

    return refresh
