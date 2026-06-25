import csv
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from banking_readonly.balance_snapshot import (
    AccountBalanceObservation,
    write_balance_snapshot,
)
from banking_readonly.config import (
    AppConfig,
    CredentialsConfig,
    DetectionConfig,
    ExportAccount,
    ExportConfig,
    RuntimeConfig,
)
from transaction_store.classification import (
    ClassificationStatus,
    can_be_auto_classified,
    classification_status,
    requires_manual_classification_review,
)
from transaction_store import database as database_module
from transaction_store.database import connect_database
from transaction_store.models import AccountDefinition
from transaction_store.parsers import (
    SPARKASSE_LEGACY_HEADERS,
    SPARKASSE_HEADERS,
    TransactionParseError,
    VOLKSBANK_LEGACY_HEADERS,
    VOLKSBANK_HEADERS,
    parse_export,
)
from transaction_store.pipeline import (
    _historical_run_id,
    import_existing_exports,
)
from transaction_store.rules import (
    CONFLICT_DESCRIPTION_PREFIX,
    ClassificationRule,
    apply_classification_rules,
    connect_rules_database,
    load_classification_rules,
    upsert_classification_rule,
)


class DatabaseConnectionTests(unittest.TestCase):
    def test_empty_sqlite_sidecars_are_discarded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "transactions.sqlite3"
            wal_path = path.with_name(f"{path.name}-wal")
            shm_path = path.with_name(f"{path.name}-shm")
            wal_path.write_bytes(b"")
            shm_path.write_bytes(b"stale index")

            database_module._discard_empty_sqlite_sidecars(path)

            self.assertFalse(wal_path.exists())
            self.assertFalse(shm_path.exists())

    def test_non_empty_sqlite_wal_is_not_discarded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "transactions.sqlite3"
            wal_path = path.with_name(f"{path.name}-wal")
            shm_path = path.with_name(f"{path.name}-shm")
            wal_path.write_bytes(b"pending")
            shm_path.write_bytes(b"stale index")

            with self.assertRaises(sqlite3.OperationalError):
                database_module._discard_empty_sqlite_sidecars(path)

            self.assertTrue(wal_path.exists())
            self.assertTrue(shm_path.exists())


def write_csv(path: Path, headers, rows, encoding="utf-8-sig"):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=encoding, newline="") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(headers)
        writer.writerows(rows)


def volksbank_row(iban="DE31384621350101206017"):
    return [
        "Hauptkonto",
        iban,
        "GENODED1WIL",
        "Bank",
        "10.06.2026",
        "10.06.2026",
        "Zahlungsbeteiligter",
        "DE00123456780000000000",
        "TESTBIC",
        "Ueberweisung",
        "Testzweck",
        "-12,34",
        "EUR",
        "100,00",
        "",
        "",
        "DE98ZZZ09999999999",
        "MANDAT-1",
    ]


def app_config(output_dir: Path) -> AppConfig:
    return AppConfig(
        login_url="https://bank.test/login",
        credentials=CredentialsConfig(
            mode="manual",
            env_file=None,
            username_variable=None,
            password_variable=None,
            username_selector=None,
            password_selector=None,
            submit_selector=None,
        ),
        export=ExportConfig(
            output_dir=output_dir,
            format="CSV",
            period="FROM_SEARCH",
            download_timeout_seconds=60,
            accounts=(
                ExportAccount(
                    "Hauptkonto",
                    "DE31384621350101206017",
                    "hauptkonto.csv",
                ),
            ),
        ),
        detection=DetectionConfig(
            success_selector="#overview",
            success_url_pattern=None,
            timeout_seconds=60,
            poll_interval_seconds=0.5,
            stable_seconds=1,
        ),
        runtime=RuntimeConfig(
            profile_dir=output_dir / "profile",
            log_dir=output_dir / "logs",
            screenshot_dir=output_dir / "screenshots",
            navigation_timeout_seconds=30,
        ),
        provider="volksbank",
    )


def sparkasse_config(output_dir: Path) -> AppConfig:
    account = ExportAccount(
        "Sichteinlagen",
        "DE29384500000000359232",
        "veranstaltungen.csv",
    )
    config = app_config(output_dir)
    return AppConfig(
        login_url=config.login_url,
        credentials=config.credentials,
        export=ExportConfig(
            output_dir=output_dir,
            format="CSV_MT940",
            period="CURRENT_VIEW",
            download_timeout_seconds=60,
            accounts=(account,),
        ),
        detection=config.detection,
        runtime=config.runtime,
        provider="sparkasse",
    )


def sparkasse_row(
    booking_date: str,
    amount: str,
    purpose: str,
):
    return [
        "DE29384500000000359232",
        booking_date,
        booking_date,
        "Gutschrift",
        purpose,
        "Zahler",
        "DE00123456780000000000",
        "12345678",
        amount,
        "EUR",
        "Umsatz gebucht",
    ]


class TransactionParserTests(unittest.TestCase):
    def test_pending_sparkasse_transaction_is_ignored_before_date_validation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "pending.csv"
            row = sparkasse_row("11.06.26", "-50,04", "Vorgemerkt")
            row[1] = "ungueltig"
            row[2] = "11.06.26"
            row[10] = "Umsatz vorgemerkt"
            write_csv(
                path,
                SPARKASSE_HEADERS,
                [
                    row,
                    sparkasse_row("10.06.26", "20,00", "Gebucht"),
                ],
            )

            parsed = parse_export(
                path,
                AccountDefinition(
                    provider="sparkasse",
                    name="Sichteinlagen",
                    number="DE29384500000000359232",
                    filename="pending.csv",
                ),
                account_balance=Decimal("200.00"),
                balance_as_of="2026-06-11",
                balance_currency="EUR",
            )

            self.assertEqual(len(parsed.transactions), 1)
            self.assertEqual(
                parsed.transactions[0].booking_date,
                "2026-06-10",
            )
            self.assertEqual(
                parsed.transactions[0].value_date,
                "2026-06-10",
            )
            self.assertEqual(
                parsed.transactions[0].account_balance,
                Decimal("200.00"),
            )

    def test_identical_rows_get_unique_stable_occurrence_ids(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "hauptkonto.csv"
            row = volksbank_row()
            older_row = volksbank_row()
            older_row[13] = "112,34"
            write_csv(path, VOLKSBANK_HEADERS, [row, older_row])
            account = AccountDefinition(
                "volksbank",
                "Hauptkonto",
                "DE31384621350101206017",
                "hauptkonto.csv",
            )

            first = parse_export(path, account)
            second = parse_export(path, account)

            self.assertEqual(len(first.transactions), 2)
            self.assertNotEqual(
                first.transactions[0].transaction_id,
                first.transactions[1].transaction_id,
            )
            self.assertEqual(
                [item.transaction_id for item in first.transactions],
                [item.transaction_id for item in second.transactions],
            )
            self.assertEqual(
                format(first.transactions[0].account_balance, ".2f"),
                "100.00",
            )
            self.assertEqual(
                format(first.transactions[1].account_balance, ".2f"),
                "112.34",
            )

    def test_inconsistent_volksbank_balance_chain_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "hauptkonto.csv"
            write_csv(
                path,
                VOLKSBANK_HEADERS,
                [volksbank_row(), volksbank_row()],
            )
            account = AccountDefinition(
                "volksbank",
                "Hauptkonto",
                "DE31384621350101206017",
                "hauptkonto.csv",
            )

            with self.assertRaises(TransactionParseError):
                parse_export(path, account)

    def test_reads_legacy_volksbank_schema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = (
                Path(temp_dir)
                / "Umsaetze_DE31384621350101206017_2023.06.07.csv"
            )
            row = volksbank_row()
            legacy_row = [
                *row[:15],
                "Alte Kategorie",
                "Nein",
                row[16],
                row[17],
            ]
            write_csv(path, VOLKSBANK_LEGACY_HEADERS, [legacy_row])
            account = AccountDefinition(
                "volksbank",
                "Hauptkonto",
                "DE31384621350101206017",
                path.name,
            )

            parsed = parse_export(path, account)

            self.assertEqual(
                format(parsed.transactions[0].account_balance, ".2f"),
                "100.00",
            )
            self.assertIn(
                "Alte Kategorie",
                parsed.transactions[0].source_info,
            )
            self.assertTrue(
                _historical_run_id(parsed).startswith("20230607T")
            )

    def test_same_booking_on_different_accounts_has_different_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_path = root / "first.csv"
            second_path = root / "second.csv"
            write_csv(first_path, VOLKSBANK_HEADERS, [volksbank_row()])
            write_csv(
                second_path,
                VOLKSBANK_HEADERS,
                [volksbank_row("DE09384621350101206025")],
            )

            first = parse_export(
                first_path,
                AccountDefinition(
                    "volksbank",
                    "Hauptkonto",
                    "DE31384621350101206017",
                    "first.csv",
                ),
            )
            second = parse_export(
                second_path,
                AccountDefinition(
                    "volksbank",
                    "Ruecklagen",
                    "DE09384621350101206025",
                    "second.csv",
                ),
            )

            self.assertNotEqual(
                first.transactions[0].transaction_id,
                second.transactions[0].transaction_id,
            )

    def test_reads_sparkasse_windows_1252_and_short_date(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "veranstaltungen.csv"
            row = [
                "DE29384500000000359232",
                "10.06.26",
                "10.06.26",
                "Gutschrift",
                "Beiträge",
                "Zahler",
                "DE00123456780000000000",
                "12345678",
                "25,00",
                "EUR",
                "Umsatz gebucht",
            ]
            write_csv(path, SPARKASSE_HEADERS, [row], encoding="cp1252")

            parsed = parse_export(
                path,
                AccountDefinition(
                    "sparkasse",
                    "Sichteinlagen",
                    "DE29384500000000359232",
                    "veranstaltungen.csv",
                ),
            )

            self.assertEqual(parsed.transactions[0].booking_date, "2026-06-10")
            self.assertEqual(
                format(parsed.transactions[0].amount, ".2f"),
                "25.00",
            )

    def test_reads_legacy_sparkasse_schema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "20230607-1013556-umsatz.CSV"
            row = [
                "DE85384500000001013556",
                "10.06.23",
                "10.06.23",
                "Gutschrift",
                "Testzweck",
                "",
                "",
                "",
                "",
                "",
                "",
                "Zahler",
                "DE00123456780000000000",
                "TESTBIC",
                "25,00",
                "EUR",
                "Umsatz gebucht",
            ]
            write_csv(
                path,
                SPARKASSE_LEGACY_HEADERS,
                [row],
                encoding="cp1252",
            )

            parsed = parse_export(
                path,
                AccountDefinition(
                    "sparkasse",
                    "Sichteinlagen - Vereinsheim",
                    "DE85384500000001013556",
                    path.name,
                ),
            )

            self.assertEqual(
                parsed.transactions[0].counterparty_account,
                "DE00123456780000000000",
            )

    def test_sparkasse_balance_anchor_is_calculated_backwards(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "veranstaltungen.csv"
            write_csv(
                path,
                SPARKASSE_HEADERS,
                [
                    sparkasse_row("11.06.26", "20,00", "Neu"),
                    sparkasse_row("10.06.26", "25,00", "Alt"),
                ],
            )

            parsed = parse_export(
                path,
                AccountDefinition(
                    "sparkasse",
                    "Sichteinlagen",
                    "DE29384500000000359232",
                    path.name,
                ),
                account_balance=Decimal("200.00"),
                balance_as_of="2026-06-11",
                balance_currency="EUR",
            )

            self.assertEqual(
                [
                    format(item.account_balance, ".2f")
                    for item in parsed.transactions
                ],
                ["200.00", "180.00"],
            )


class ClassificationTests(unittest.TestCase):
    def test_empty_classification_can_be_automatically_classified(self):
        transaction = {
            "transaction_type": " ",
            "top_category": "",
            "sub_category": None,
            "sphere": "",
            "professional_description": "",
        }

        self.assertEqual(
            classification_status(transaction),
            ClassificationStatus.UNCLASSIFIED,
        )
        self.assertTrue(can_be_auto_classified(transaction))
        self.assertFalse(requires_manual_classification_review(transaction))

    def test_all_required_fields_are_fully_classified(self):
        transaction = {
            "transaktionstyp": "Einnahme",
            "oberkategorie": "Spielbetrieb",
            "unterkategorie": "Eintritt",
            "sphaere": "Ideeller Bereich",
            "fachliche_beschreibung": "",
        }

        self.assertEqual(
            classification_status(transaction),
            ClassificationStatus.FULLY_CLASSIFIED,
        )
        self.assertFalse(can_be_auto_classified(transaction))
        self.assertFalse(requires_manual_classification_review(transaction))

    def test_partial_required_fields_require_manual_review(self):
        transaction = {"transaction_type": "Ausgabe"}

        self.assertEqual(
            classification_status(transaction),
            ClassificationStatus.INCOMPLETELY_CLASSIFIED,
        )
        self.assertFalse(can_be_auto_classified(transaction))
        self.assertTrue(requires_manual_classification_review(transaction))

    def test_description_alone_blocks_automatic_classification(self):
        transaction = {"professional_description": "Manuelle Notiz"}

        self.assertEqual(
            classification_status(transaction),
            ClassificationStatus.INCOMPLETELY_CLASSIFIED,
        )
        self.assertFalse(can_be_auto_classified(transaction))


class TransactionPipelineTests(unittest.TestCase):
    def test_sparkasse_snapshot_backfills_entire_overlapping_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            old_run = export_dir / "20260610T070000_000001Z"
            new_run = export_dir / "20260611T070000_000002Z"
            write_csv(
                old_run / "veranstaltungen.csv",
                SPARKASSE_HEADERS,
                [
                    sparkasse_row("10.06.26", "25,00", "Alt"),
                    sparkasse_row("09.06.26", "-10,00", "Aelter"),
                ],
            )
            write_csv(
                new_run / "veranstaltungen.csv",
                SPARKASSE_HEADERS,
                [
                    sparkasse_row("11.06.26", "20,00", "Neu"),
                    sparkasse_row("10.06.26", "25,00", "Alt"),
                ],
            )
            write_balance_snapshot(
                new_run,
                "sparkasse",
                {
                    "DE29384500000000359232": AccountBalanceObservation(
                        account_name="Sichteinlagen",
                        account_number="DE29384500000000359232",
                        balance=Decimal("200.00"),
                        currency="EUR",
                        captured_at=datetime(
                            2026,
                            6,
                            11,
                            12,
                            0,
                            tzinfo=timezone.utc,
                        ),
                    )
                },
            )

            summary = import_existing_exports(
                [sparkasse_config(export_dir)],
                root / "data" / "transactions",
            )

            connection = connect_database(summary.database_path)
            try:
                rows = connection.execute(
                    """
                    SELECT booking_date, account_balance_minor
                    FROM transactions
                    ORDER BY booking_date DESC
                    """
                ).fetchall()
                account = connection.execute(
                    """
                    SELECT current_balance_minor, balance_as_of
                    FROM accounts
                    """
                ).fetchone()
            finally:
                connection.close()

            self.assertEqual(
                [
                    (row["booking_date"], row["account_balance_minor"])
                    for row in rows
                ],
                [
                    ("2026-06-11", 20000),
                    ("2026-06-10", 18000),
                    ("2026-06-09", 15500),
                ],
            )
            self.assertEqual(account["current_balance_minor"], 20000)
            self.assertEqual(account["balance_as_of"], "2026-06-11")

            connection = sqlite3.connect(summary.database_path)
            try:
                connection.execute(
                    """
                    UPDATE transactions
                    SET account_balance_minor = 1
                    WHERE booking_date = '2026-06-09'
                    """
                )
                connection.commit()
            finally:
                connection.close()

            import_existing_exports(
                [sparkasse_config(export_dir)],
                root / "data" / "transactions",
            )
            connection = sqlite3.connect(summary.database_path)
            try:
                corrected = connection.execute(
                    """
                    SELECT account_balance_minor
                    FROM transactions
                    WHERE booking_date = '2026-06-09'
                    """
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(corrected, 15500)

    def test_repeated_exports_are_archived_but_not_duplicated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            for run_id in (
                "20260610T070000_000001Z",
                "20260610T080000_000002Z",
            ):
                write_csv(
                    export_dir / run_id / "hauptkonto.csv",
                    VOLKSBANK_HEADERS,
                    [volksbank_row()],
                )

            store_root = root / "data" / "transactions"
            summary = import_existing_exports(
                [app_config(export_dir)],
                store_root,
            )

            self.assertEqual(summary.runs, 2)
            self.assertEqual(summary.source_files, 2)
            self.assertEqual(summary.new_transactions, 1)
            self.assertEqual(summary.existing_transactions, 1)
            self.assertEqual(summary.total_transactions, 1)

            connection = sqlite3.connect(summary.database_path)
            try:
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM transaction_sources"
                    ).fetchone()[0],
                    2,
                )
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM vorgaenge"
                    ).fetchone()[0],
                    0,
                )
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM transaktion_vorgaenge"
                    ).fetchone()[0],
                    0,
                )
            finally:
                connection.close()

            with summary.normalized_path.open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                rows = list(csv.reader(handle, delimiter=";"))
            self.assertEqual(
                rows[0],
                [
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
                ],
            )
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1][5], "Testzweck")
            self.assertEqual(rows[1][7], "100.00")
            self.assertEqual(rows[1][8], "100.00")
            self.assertEqual(rows[1][9], "1")
            self.assertEqual(rows[1][-2], "unklassifiziert")
            self.assertEqual(rows[1][-1], "")
            manifests = list(
                (store_root / "archive" / "manifests").rglob("*.json")
            )
            self.assertEqual(len(manifests), 2)

    def test_reimport_preserves_manual_classification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [volksbank_row()],
            )
            store_root = root / "data" / "transactions"
            config = app_config(export_dir)
            first = import_existing_exports([config], store_root)

            connection = sqlite3.connect(first.database_path)
            try:
                connection.execute(
                    """
                    UPDATE transactions
                    SET transaction_type = 'Ausgabe'
                    """
                )
                connection.commit()
            finally:
                connection.close()

            second = import_existing_exports([config], store_root)
            connection = sqlite3.connect(second.database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT * FROM normalized_transactions"
                ).fetchone()
            finally:
                connection.close()

            self.assertEqual(row["transaktionstyp"], "Ausgabe")
            self.assertEqual(
                row["klassifikationsstatus"],
                "unvollstaendig_klassifiziert",
            )
            self.assertEqual(row["budget_id"], "")
            self.assertFalse(can_be_auto_classified(row))

    def test_overlapping_exports_with_different_balances_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            first_row = volksbank_row()
            second_row = volksbank_row()
            second_row[13] = "99,00"
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [first_row],
            )
            write_csv(
                export_dir
                / "20260611T070000_000002Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [second_row],
            )

            with self.assertRaises(RuntimeError):
                import_existing_exports(
                    [app_config(export_dir)],
                    root / "data" / "transactions",
                )

    def test_budget_id_matches_budget_row_and_season_starts_in_july(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            june_row = volksbank_row()
            june_row[10] = "Saisonabgrenzung Juni"
            july_row = volksbank_row()
            july_row[4] = "01.07.2026"
            july_row[5] = "01.07.2026"
            july_row[10] = "Saisonabgrenzung Juli"
            june_row[13] = "112,34"
            write_csv(
                export_dir
                / "20260701T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [july_row, june_row],
            )
            summary = import_existing_exports(
                [app_config(export_dir)],
                root / "data" / "transactions",
            )

            connection = connect_database(summary.database_path)
            try:
                connection.execute(
                    """
                    UPDATE transactions
                    SET top_category = 'Spielbetrieb',
                        sub_category = 'Eintritt'
                    """
                )
                connection.execute(
                    """
                    INSERT INTO budgets (
                        saison, oberkategorie, unterkategorie,
                        einnahmen, ausgaben
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    ("2025/2026", "Spielbetrieb", "Eintritt", 250, 1000),
                )
                rows = connection.execute(
                    """
                    SELECT datum, budget_id
                    FROM normalized_transactions
                    ORDER BY datum
                    """
                ).fetchall()
                budget = connection.execute(
                    """
                    SELECT *
                    FROM budgets
                    WHERE saison = '2025/2026'
                    """
                ).fetchone()
            finally:
                connection.close()

            self.assertEqual(rows[0]["datum"], "2026-06-10")
            self.assertEqual(rows[0]["budget_id"], budget["budget_id"])
            self.assertEqual(rows[1]["datum"], "2026-07-01")
            self.assertNotEqual(rows[1]["budget_id"], budget["budget_id"])
            self.assertIn("2026_2027", rows[1]["budget_id"])
            self.assertEqual(budget["budget"], 750)

    def test_transaction_link_tables_support_many_to_many_assignments(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [volksbank_row()],
            )
            summary = import_existing_exports(
                [app_config(export_dir)],
                root / "data" / "transactions",
            )

            connection = connect_database(summary.database_path)
            try:
                transaktions_id = connection.execute(
                    """
                    SELECT transaktions_id
                    FROM normalized_transactions
                    """
                ).fetchone()["transaktions_id"]
                connection.executemany(
                    """
                    INSERT INTO vorgaenge (
                        vorgangs_id, vorgangstyp, status
                    ) VALUES (?, '', 'in_bearbeitung')
                    """,
                    (
                        ("vorgang_1",),
                        ("vorgang_2",),
                    ),
                )
                connection.executemany(
                    """
                    INSERT INTO transaktion_vorgaenge (
                        transaktions_id, vorgangs_id
                    ) VALUES (?, ?)
                    """,
                    (
                        (transaktions_id, "vorgang_1"),
                        (transaktions_id, "vorgang_2"),
                    ),
                )
                now = "2026-06-15T00:00:00+00:00"
                connection.executemany(
                    """
                    INSERT INTO belege (
                        beleg_id, dateiname, dateipfad, dateityp,
                        dateigroesse, datei_sha256, vorhanden, quelle,
                        erstellt_am, aktualisiert_am
                    ) VALUES (?, ?, ?, '', NULL, '', 0, 'manual', ?, ?)
                    """,
                    (
                        (
                            "beleg_1",
                            "beleg_1",
                            str((root / "belege" / "beleg_1").resolve()),
                            now,
                            now,
                        ),
                        (
                            "beleg_2",
                            "beleg_2",
                            str((root / "belege" / "beleg_2").resolve()),
                            now,
                            now,
                        ),
                    ),
                )
                connection.executemany(
                    """
                    INSERT INTO vorgang_belege (
                        vorgangs_id, beleg_id, erstellt_am
                    ) VALUES (?, ?, ?)
                    """,
                    (
                        ("vorgang_1", "beleg_1", now),
                        ("vorgang_1", "beleg_2", now),
                        ("vorgang_2", "beleg_1", now),
                    ),
                )
                self.assertEqual(
                    connection.execute(
                        """
                        SELECT COUNT(*)
                        FROM transaktion_vorgaenge
                        """
                    ).fetchone()[0],
                    2,
                )
                self.assertEqual(
                    connection.execute(
                        """
                        SELECT COUNT(*)
                        FROM vorgang_belege
                        """
                    ).fetchone()[0],
                    3,
                )
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        """
                        INSERT INTO transaktion_vorgaenge (
                            transaktions_id, vorgangs_id
                        ) VALUES (?, ?)
                        """,
                        (transaktions_id, "vorgang_1"),
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        """
                        INSERT INTO transaktion_vorgaenge (
                            transaktions_id, vorgangs_id
                        ) VALUES (?, ?)
                        """,
                        (transaktions_id, "vorgang_unbekannt"),
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        """
                        INSERT INTO vorgang_belege (
                            vorgangs_id, beleg_id, erstellt_am
                        ) VALUES (?, ?, ?)
                        """,
                        ("vorgang_unbekannt", "beleg_1", now),
                    )
            finally:
                connection.close()

    def test_version_ten_document_links_are_migrated_to_vorgaenge(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [volksbank_row()],
            )
            summary = import_existing_exports(
                [app_config(export_dir)],
                root / "data" / "transactions",
            )
            connection = connect_database(summary.database_path)
            try:
                transaction_id = connection.execute(
                    "SELECT transaction_id FROM transactions"
                ).fetchone()[0]
                connection.execute(
                    """
                    INSERT INTO vorgaenge (
                        vorgangs_id, vorgangstyp, status
                    ) VALUES ('vorgang_legacy', '', 'in_bearbeitung')
                    """
                )
                connection.execute(
                    """
                    INSERT INTO transaktion_vorgaenge (
                        transaktions_id, vorgangs_id
                    ) VALUES (?, 'vorgang_legacy')
                    """,
                    (transaction_id,),
                )
                connection.execute("DROP TABLE vorgang_belege")
                connection.execute("DROP TABLE belege")
                connection.execute(
                    """
                    CREATE TABLE transaktion_belege (
                        transaktions_id TEXT NOT NULL,
                        beleg_id TEXT NOT NULL,
                        PRIMARY KEY (transaktions_id, beleg_id)
                    )
                    """
                )
                connection.execute(
                    """
                    INSERT INTO transaktion_belege (
                        transaktions_id, beleg_id
                    ) VALUES (?, 'legacy_beleg')
                    """,
                    (transaction_id,),
                )
                connection.execute("UPDATE schema_info SET version = 10")
                connection.commit()
            finally:
                connection.close()

            migrated = connect_database(summary.database_path)
            try:
                document = migrated.execute(
                    """
                    SELECT beleg_id, dateipfad, quelle, vorhanden
                    FROM belege
                    WHERE beleg_id = 'legacy_beleg'
                    """
                ).fetchone()
                link = migrated.execute(
                    """
                    SELECT vorgangs_id, beleg_id
                    FROM vorgang_belege
                    WHERE beleg_id = 'legacy_beleg'
                    """
                ).fetchone()
                old_table = migrated.execute(
                    """
                    SELECT 1
                    FROM sqlite_master
                    WHERE type = 'table'
                      AND name = 'transaktion_belege'
                    """
                ).fetchone()
            finally:
                migrated.close()

        self.assertEqual("legacy_beleg", document["beleg_id"])
        self.assertTrue(document["dateipfad"].endswith("legacy_beleg"))
        self.assertEqual("migration", document["quelle"])
        self.assertEqual(0, document["vorhanden"])
        self.assertTrue(link["vorgangs_id"].startswith("vorgang_"))
        self.assertEqual("legacy_beleg", link["beleg_id"])
        self.assertIsNone(old_table)

    def test_trainer_bsv_1_rule_classifies_only_unclassified_transactions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            row = volksbank_row()
            row[10] = (
                "Vergütung Trainer BSV 1 /*DA-56* "
                "IBAN: DE15384621357116149014"
            )
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [row],
            )
            summary = import_existing_exports(
                [app_config(export_dir)],
                root / "data" / "transactions",
            )

            connection = sqlite3.connect(summary.database_path)
            connection.row_factory = sqlite3.Row
            rules_connection = connect_rules_database(
                summary.database_path.parent / "rules.sqlite3"
            )
            try:
                classified = connection.execute(
                    "SELECT * FROM normalized_transactions"
                ).fetchone()
                self.assertEqual(classified["transaktionstyp"], "Vergütung")
                self.assertEqual(
                    classified["oberkategorie"],
                    "Personal und Vergütungen",
                )
                self.assertEqual(
                    classified["unterkategorie"],
                    "Vergütungen - BSV 1",
                )
                self.assertEqual(classified["sphaere"], "Ideeller Bereich")
                self.assertEqual(
                    classified["fachliche_beschreibung"],
                    "Vergütung Trainer BSV 1",
                )
                self.assertEqual(
                    classified["klassifikationsstatus"],
                    "vollstaendig_klassifiziert",
                )
                connection.execute(
                    """
                    UPDATE transactions
                    SET transaction_type = 'Manuell',
                        top_category = '',
                        sub_category = '',
                        sphere = '',
                        professional_description = ''
                    """
                )
                rules = load_classification_rules(rules_connection)
                self.assertEqual(
                    apply_classification_rules(connection, rules),
                    0,
                )
                protected = connection.execute(
                    """
                    SELECT transaction_type, top_category
                    FROM transactions
                    """
                ).fetchone()
                self.assertEqual(protected["transaction_type"], "Manuell")
                self.assertEqual(protected["top_category"], "")
            finally:
                connection.close()
                rules_connection.close()

    def test_co_trainer_bsv_1_rule_uses_requested_description(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            row = volksbank_row()
            row[10] = (
                "Vergütung Co Trainer BSV 1 /*DA-54* "
                "IBAN: DE14370502991021017602"
            )
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [row],
            )
            summary = import_existing_exports(
                [app_config(export_dir)],
                root / "data" / "transactions",
            )

            connection = sqlite3.connect(summary.database_path)
            connection.row_factory = sqlite3.Row
            try:
                classified = connection.execute(
                    "SELECT * FROM normalized_transactions"
                ).fetchone()
            finally:
                connection.close()

            self.assertEqual(classified["transaktionstyp"], "Vergütung")
            self.assertEqual(
                classified["oberkategorie"],
                "Personal und Vergütungen",
            )
            self.assertEqual(
                classified["unterkategorie"],
                "Vergütungen - BSV 1",
            )
            self.assertEqual(classified["sphaere"], "Ideeller Bereich")
            self.assertEqual(
                classified["fachliche_beschreibung"],
                "Vergütung Co-Trainer BSV 1",
            )
            self.assertEqual(
                classified["klassifikationsstatus"],
                "vollstaendig_klassifiziert",
            )

    def test_multiple_matching_rules_only_write_conflict_description(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            export_dir = root / "exports"
            row = volksbank_row()
            row[10] = "Vergütung Trainer BSV 1"
            write_csv(
                export_dir
                / "20260610T070000_000001Z"
                / "hauptkonto.csv",
                VOLKSBANK_HEADERS,
                [row],
            )
            store_root = root / "data" / "transactions"
            rules_connection = connect_rules_database(
                store_root / "database" / "rules.sqlite3"
            )
            try:
                upsert_classification_rule(
                    rules_connection,
                    ClassificationRule(
                        rule_id="regel_003_testkonflikt",
                        name="Regel3",
                        enabled=True,
                        match_field="purpose",
                        match_operator="contains",
                        match_value="Trainer BSV 1",
                        transaction_type="Andere Vergütung",
                        top_category="Andere Kategorie",
                        sub_category="Andere Unterkategorie",
                        sphere="Zweckbetrieb",
                        professional_description="Andere Beschreibung",
                    ),
                )
                rules_connection.commit()
            finally:
                rules_connection.close()

            summary = import_existing_exports(
                [app_config(export_dir)],
                store_root,
            )
            connection = sqlite3.connect(summary.database_path)
            connection.row_factory = sqlite3.Row
            try:
                result = connection.execute(
                    "SELECT * FROM normalized_transactions"
                ).fetchone()
            finally:
                connection.close()

            self.assertEqual(result["transaktionstyp"], "")
            self.assertEqual(result["oberkategorie"], "")
            self.assertEqual(result["unterkategorie"], "")
            self.assertEqual(result["sphaere"], "")
            self.assertEqual(
                result["fachliche_beschreibung"],
                CONFLICT_DESCRIPTION_PREFIX + "Regel1, Regel3",
            )
            self.assertEqual(
                result["klassifikationsstatus"],
                "unvollstaendig_klassifiziert",
            )

    def test_database_version_two_is_migrated_without_changing_ids(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "transactions.sqlite3"
            connection = sqlite3.connect(path)
            try:
                connection.executescript(
                    """
                    CREATE TABLE schema_info (version INTEGER NOT NULL);
                    INSERT INTO schema_info(version) VALUES (2);
                    CREATE TABLE transactions (
                        transaction_id TEXT PRIMARY KEY,
                        fingerprint TEXT NOT NULL,
                        occurrence INTEGER NOT NULL,
                        provider TEXT NOT NULL,
                        account_id TEXT NOT NULL,
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
                        UNIQUE(fingerprint, occurrence)
                    );
                    INSERT INTO transactions VALUES (
                        'tx_existing', 'fp_existing', 1, 'volksbank',
                        'acct_existing', 'Hauptkonto',
                        'DE31384621350101206017', '2026-06-10',
                        '2026-06-10', 'Zahlungsbeteiligter', '-12.34',
                        'EUR', 'Ueberweisung', 'Testzweck', -1234, '',
                        '', '', '', '{}', '2026-06-10T00:00:00+00:00'
                    );
                    """
                )
            finally:
                connection.close()

            migrated = connect_database(path)
            try:
                self.assertEqual(
                    migrated.execute(
                        "SELECT version FROM schema_info"
                    ).fetchone()[0],
                    13,
                )
                row = migrated.execute(
                    "SELECT * FROM normalized_transactions"
                ).fetchone()
                self.assertEqual(
                    row["transaktions_id"],
                    "tx_existing",
                )
                self.assertEqual(
                    row["klassifikationsstatus"],
                    "unklassifiziert",
                )
                self.assertEqual(row["budget_id"], "")
                vorgang = migrated.execute(
                    """
                    SELECT
                        v.vorgangs_id,
                        v.vorgangstyp,
                        v.status,
                        tv.transaktions_id
                    FROM vorgaenge AS v
                    JOIN transaktion_vorgaenge AS tv
                        ON tv.vorgangs_id = v.vorgangs_id
                    """
                ).fetchone()
                self.assertIsNone(vorgang)
                self.assertEqual(
                    migrated.execute(
                        """
                        SELECT COUNT(*)
                        FROM vorgaenge
                        WHERE vorgangs_id = 'vorgang_tx_existing'
                        """
                    ).fetchone()[0],
                    0,
                )
                budget_columns = [
                    item["name"]
                    for item in migrated.execute(
                        "PRAGMA table_xinfo(budgets)"
                    )
                ]
                self.assertEqual(
                    budget_columns,
                    [
                        "saison",
                        "oberkategorie",
                        "unterkategorie",
                        "einnahmen",
                        "ausgaben",
                        "budget",
                        "budget_id",
                    ],
                )
                self.assertEqual(
                    [
                        item["name"]
                        for item in migrated.execute(
                            "PRAGMA table_info(transaktion_vorgaenge)"
                        )
                    ],
                    ["transaktions_id", "vorgangs_id"],
                )
                self.assertEqual(
                    [
                        item["name"]
                        for item in migrated.execute(
                            "PRAGMA table_info(vorgang_belege)"
                        )
                    ],
                    ["vorgangs_id", "beleg_id", "erstellt_am"],
                )
                self.assertIsNone(
                    migrated.execute(
                        """
                        SELECT 1
                        FROM sqlite_master
                        WHERE type = 'table'
                          AND name = 'transaktion_belege'
                        """
                    ).fetchone()
                )
            finally:
                migrated.close()

    def test_database_version_seven_removes_pending_sparkasse_transactions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "transactions.sqlite3"
            connection = connect_database(path)
            try:
                connection.execute(
                    """
                    INSERT INTO accounts (
                        account_id, provider, account_name, account_number
                    ) VALUES (
                        'acct_sparkasse', 'sparkasse', 'Vereinsheim',
                        'DE85384500000001013556'
                    )
                    """
                )
                connection.execute(
                    """
                    INSERT INTO source_files (
                        file_id, provider, export_run_id, original_filename,
                        original_path, archive_path, file_sha256, encoding,
                        delimiter, row_count, imported_at
                    ) VALUES (
                        'file_pending', 'sparkasse', 'run_pending',
                        'pending.csv', 'pending.csv', 'pending.csv',
                        'hash_pending', 'utf-8', ';', 2,
                        '2026-06-12T00:00:00+00:00'
                    )
                    """
                )
                for transaction_id, source_info in (
                    ("tx_pending", "Umsatz vorgemerkt"),
                    ("tx_booked", "Umsatz gebucht"),
                ):
                    connection.execute(
                        """
                        INSERT INTO transactions (
                            transaction_id, fingerprint, occurrence, provider,
                            account_id, account_name, account_number,
                            booking_date, value_date, counterparty, amount,
                            currency, booking_text, purpose, amount_minor,
                            counterparty_account, creditor_id,
                            mandate_reference, source_info, raw_fields_json,
                            first_seen_at
                        ) VALUES (
                            ?, ?, 1, 'sparkasse', 'acct_sparkasse',
                            'Vereinsheim', 'DE85384500000001013556',
                            '2026-06-12', '2026-06-12', '', '-10.00',
                            'EUR', 'Einzug', 'Test', -1000, '', '', '',
                            ?, '{}', '2026-06-12T00:00:00+00:00'
                        )
                        """,
                        (
                            transaction_id,
                            f"fp_{transaction_id}",
                            source_info,
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO transaction_sources (
                            transaction_id, file_id, source_row_number
                        ) VALUES (?, 'file_pending', ?)
                        """,
                        (
                            transaction_id,
                            2 if transaction_id == "tx_pending" else 3,
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO vorgaenge (
                            vorgangs_id, vorgangstyp, status
                        ) VALUES (?, '', 'in_bearbeitung')
                        """,
                        (f"vorgang_{transaction_id}",),
                    )
                    connection.execute(
                        """
                        INSERT INTO transaktion_vorgaenge (
                            transaktions_id, vorgangs_id
                        ) VALUES (?, ?)
                        """,
                        (transaction_id, f"vorgang_{transaction_id}"),
                    )
                connection.execute("UPDATE schema_info SET version = 7")
                connection.commit()
            finally:
                connection.close()

            migrated = connect_database(path)
            try:
                self.assertEqual(
                    migrated.execute(
                        "SELECT version FROM schema_info"
                    ).fetchone()[0],
                    13,
                )
                self.assertEqual(
                    [
                        row["transaction_id"]
                        for row in migrated.execute(
                            "SELECT transaction_id FROM transactions"
                        )
                    ],
                    ["tx_booked"],
                )
                self.assertEqual(
                    migrated.execute(
                        """
                        SELECT COUNT(*)
                        FROM transaction_sources
                        WHERE transaction_id = 'tx_pending'
                        """
                    ).fetchone()[0],
                    0,
                )
                self.assertEqual(
                    migrated.execute(
                        """
                        SELECT row_count
                        FROM source_files
                        WHERE file_id = 'file_pending'
                        """
                    ).fetchone()[0],
                    1,
                )
                self.assertEqual(
                    migrated.execute(
                        """
                        SELECT COUNT(*)
                        FROM vorgaenge
                        WHERE vorgangs_id = 'vorgang_tx_pending'
                        """
                    ).fetchone()[0],
                    0,
                )
                self.assertEqual(
                    migrated.execute(
                        """
                        SELECT COUNT(*)
                        FROM vorgaenge
                        WHERE vorgangs_id = 'vorgang_tx_booked'
                        """
                    ).fetchone()[0],
                    0,
                )
            finally:
                migrated.close()


if __name__ == "__main__":
    unittest.main()
