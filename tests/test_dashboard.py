import base64
import json
import re
import sqlite3
import subprocess
import tempfile
import threading
import unittest
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from banking_dashboard import DashboardDataStore, create_server
from banking_dashboard.mail_integration import InboxMailStore, MailAttachmentContent
from banking_dashboard.server import (
    default_transaction_period,
    fallback_mail_vorgang_analysis,
)
from transaction_store.database import (
    TERMIN_STATUS_CANCELLED,
    TERMIN_STATUS_COMPLETED,
    connect_database,
)
from transaction_store.rules import (
    connect_rules_database,
    list_classification_rules,
    list_completion_rules,
)


class FakeDashboardMailBackend:
    def __init__(self):
        self.message = {
            "id": "mail-1",
            "subject": "Rechnung und Termin",
            "fromName": "Stadtwerke",
            "fromAddress": "rechnung@example.test",
            "to": ["kasse@bsv-bielstein.de"],
            "receivedDateTime": "2026-06-18T09:00:00+02:00",
            "body": (
                "Bitte Rechnung pruefen. Termin am 2026-07-03 um 18 Uhr."
            ),
            "bodyPreview": "Bitte Rechnung pruefen.",
            "folderName": "Posteingang",
            "category": "",
            "isRead": False,
            "attachmentCount": 2,
            "attachments": [
                {
                    "attachmentIndex": 1,
                    "filename": "rechnung.pdf",
                    "contentType": "application/pdf",
                    "size": 17,
                    "text": "Rechnung 42,00 EUR",
                },
                {
                    "attachmentIndex": 2,
                    "filename": "zahlungsziel.txt",
                    "contentType": "text/plain",
                    "size": 24,
                    "text": "Zahlungsziel 2026-06-30",
                }
            ],
        }

    def list_messages(self):
        return [dict(self.message)]

    def read_message(self, entry_id):
        if entry_id != "mail-1":
            raise LookupError("Mail wurde nicht gefunden.")
        return dict(self.message)

    def read_attachment(self, entry_id, attachment_index):
        if entry_id != "mail-1" or attachment_index not in {1, 2}:
            raise LookupError("Anhang wurde nicht gefunden.")
        if attachment_index == 2:
            return MailAttachmentContent(
                content=b"Zahlungsziel 2026-06-30",
                content_type="text/plain",
                filename="zahlungsziel.txt",
            )
        return MailAttachmentContent(
            content=b"%PDF-1.4 Rechnung",
            content_type="application/pdf",
            filename="rechnung.pdf",
        )

    def set_category(self, entry_id, category):
        self.message["category"] = category

    def mark_read(self, entry_id):
        self.message["isRead"] = True

    def delete_message(self, entry_id):
        self.message["deleted"] = True

    def send_reply(self, entry_id, body, to_recipients=None):
        self.message["lastReply"] = {
            "body": body,
            "to_recipients": to_recipients,
        }


class FakeMailVorgangAnalyzer:
    def analyze(self, message):
        return {
            "vorgang": {
                "title": "Rechnung Stadtwerke",
                "description": "Rechnung pruefen und Termin notieren.",
                "vorgangstyp": "Rechnung",
            },
            "documents": [
                {
                    "attachment_index": 1,
                    "category": "rechnungen",
                    "filename": "rechnung.pdf",
                    "document_date": "2026-06-18",
                    "amount": "42,00 EUR",
                    "issuer": "Stadtwerke",
                    "recipient": "BSV Viktoria Bielstein",
                    "description": "Stromrechnung",
                    "confidence": 0.9,
                    "enabled": True,
                },
                {
                    "attachment_index": 2,
                    "category": "sonstige_dokumente",
                    "filename": "zahlungsziel.txt",
                    "document_date": "",
                    "amount": "",
                    "issuer": "Stadtwerke",
                    "recipient": "BSV Viktoria Bielstein",
                    "description": "Zahlungsziel",
                    "confidence": 0.7,
                    "enabled": True,
                }
            ],
            "todos": [
                {
                    "title": "Rechnung pruefen",
                    "description": "Betrag und Faelligkeit pruefen.",
                    "due_date": "2026-06-25",
                    "priority": "hoch",
                    "confidence": 0.8,
                    "enabled": True,
                }
            ],
            "termine": [
                {
                    "title": "Termin Stadtwerke",
                    "description": "Ruecksprache",
                    "starts_at": "2026-07-03T18:00:00+02:00",
                    "ends_at": "",
                    "location": "Vereinsheim",
                    "confidence": 0.7,
                    "enabled": True,
                }
            ],
            "source": "test",
            "model": "fake",
        }


class MailAnalysisFallbackTests(unittest.TestCase):
    def test_generated_subject_uses_mail_context_for_event_title(self):
        analysis = fallback_mail_vorgang_analysis(
            {
                "subject": "AM_25-2026",
                "body": (
                    "Hallo zusammen,\n"
                    "Tag des Maedchenfussballs in Bielstein - "
                    "Nachwuchs Bayer 04 kommt\n"
                    "Samstag, den 04.07.2026 ab 09.30 Uhr rund um die "
                    "Dr. Kind Arena\n"
                    "Hiermit laden wir recht herzlich alle "
                    "fussballbegeisterten Maedchen ein.\n"
                    "Anmeldungen werden unter maedchen@example.test "
                    "entgegengenommen."
                ),
                "attachments": [],
            }
        )

        self.assertEqual(
            "Tag des Maedchenfussballs in Bielstein - "
            "Nachwuchs Bayer 04 kommt",
            analysis["vorgang"]["title"],
        )
        self.assertEqual(
            "Tag des Maedchenfussballs in Bielstein - "
            "Nachwuchs Bayer 04 kommt",
            analysis["termine"][0]["title"],
        )
        self.assertEqual(
            "2026-07-04T09:30:00",
            analysis["termine"][0]["starts_at"],
        )
        self.assertEqual("Dr. Kind Arena", analysis["termine"][0]["location"])

    def test_mail_prefix_is_not_used_as_termin_title(self):
        analysis = fallback_mail_vorgang_analysis(
            {
                "subject": "Email zu Tag des Maedchenfussballs",
                "body": (
                    "Tag des Maedchenfussballs\n"
                    "Samstag, den 04.07.2026 ab 09.30 Uhr"
                ),
                "attachments": [],
            }
        )

        self.assertEqual(
            "Tag des Maedchenfussballs",
            analysis["termine"][0]["title"],
        )


class FakeDashboardSpamScorer:
    model = "fake-spam"

    def score(self, message):
        return {
            "probability": 0.01,
            "source": "test",
            "reasons": ["Testscore"],
        }


def create_dashboard_database(path: Path) -> None:
    connection = connect_database(path)
    try:
        connection.execute(
            """
            INSERT INTO accounts (
                account_id, provider, account_name, account_number,
                current_balance_minor, balance_currency, balance_as_of,
                balance_run_id
            ) VALUES (
                'acct_test', 'testbank', 'Hauptkonto', 'DE001',
                2500, 'EUR', '2026-06-10', '20260611T080000_000001Z'
            )
            """
        )
        rows = (
            (
                "tx_older",
                "fp_older",
                "2026-05-10",
                "Älterer Verein",
                "Älterer Zweck",
                "-12.34",
                -1234,
                '{"Originalfeld": "Rohwert"}',
            ),
            (
                "tx_newer",
                "fp_newer",
                "2026-06-10",
                "Neuer Verein",
                "Neuer Zweck",
                "25.00",
                2500,
                '{"Originalfeld": "Weiterer Wert"}',
            ),
        )
        for (
            transaction_id,
            fingerprint,
            booking_date,
            counterparty,
            purpose,
            amount,
            amount_minor,
            raw_fields,
        ) in rows:
            connection.execute(
                """
                INSERT INTO transactions (
                    transaction_id, fingerprint, occurrence, provider,
                    account_id, account_name, account_number, booking_date,
                    value_date, counterparty, amount, currency, booking_text,
                    purpose, amount_minor, counterparty_account, creditor_id,
                    mandate_reference, source_info, raw_fields_json,
                    first_seen_at, transaction_type, top_category,
                    sub_category, sphere, professional_description
                    , account_balance_minor
                ) VALUES (
                    ?, ?, 1, 'testbank', 'acct_test', 'Hauptkonto', 'DE001',
                    ?, ?, ?, ?, 'EUR', 'Überweisung', ?, ?, 'DE002',
                    'creditor_1', 'mandate_1', 'Testquelle', ?,
                    '2026-06-11T08:00:00+00:00', 'Ausgabe',
                    'Spielbetrieb', 'Eintritt', 'Zweckbetrieb',
                    'Testbeschreibung', ?
                )
                """,
                (
                    transaction_id,
                    fingerprint,
                    booking_date,
                    booking_date,
                    counterparty,
                    amount,
                    purpose,
                    amount_minor,
                    raw_fields,
                    2500 if transaction_id == "tx_newer" else -1234,
                ),
            )
        connection.execute(
            """
            INSERT INTO source_files (
                file_id, provider, export_run_id, original_filename,
                original_path, archive_path, file_sha256, encoding,
                delimiter, row_count, imported_at
            ) VALUES (
                'src_test', 'testbank', '20260611T080000_000001Z',
                'test.csv', 'test.csv', 'archive/test.csv', 'hash',
                'utf-8', ';', 2, '2026-06-11T08:00:00+00:00'
            )
            """
        )
        connection.execute(
            """
            INSERT INTO transaction_sources (
                transaction_id, file_id, source_row_number
            ) VALUES ('tx_newer', 'src_test', 2)
            """
        )
        for transaction_id, vorgangstyp in (
            ("tx_older", "Ausgabe"),
            ("tx_newer", "Ausgabe"),
        ):
            connection.execute(
                """
                INSERT INTO vorgaenge (
                    vorgangs_id, titel, beschreibung, vorgangstyp,
                    status, erstellt_am, aktualisiert_am
                ) VALUES (?, '', '', ?, 'in_bearbeitung',
                    '2026-06-11T08:00:00+00:00',
                    '2026-06-11T08:00:00+00:00')
                """,
                (f"vorgang_{transaction_id}", vorgangstyp),
            )
            connection.execute(
                """
                INSERT INTO transaktion_vorgaenge (
                    transaktions_id, vorgangs_id
                ) VALUES (?, ?)
                """,
                (transaction_id, f"vorgang_{transaction_id}"),
            )
        connection.execute(
            """
            INSERT INTO transaction_splits (
                split_id, transaction_id, amount_minor, description,
                transaction_type, top_category, sub_category, sphere,
                professional_description, vorgangs_id, created_at, updated_at
            ) VALUES (
                'split_tx_newer_1', 'tx_newer', 1500,
                'Teilbetrag Eintritt', 'Einnahme', 'Spielbetrieb',
                'Eintritt', 'Zweckbetrieb', 'Split-Test',
                'vorgang_tx_newer', '2026-06-11T08:00:00+00:00',
                '2026-06-11T08:00:00+00:00'
            )
            """
        )
        connection.execute(
            """
            INSERT INTO belege (
                beleg_id, dateiname, dateipfad, dateityp,
                dateigroesse, datei_sha256, vorhanden, quelle,
                erstellt_am, aktualisiert_am
            ) VALUES (
                'beleg_1', 'beleg_1.pdf', ?, 'application/pdf',
                12, 'hash_beleg_1', 0, 'manual',
                '2026-06-11T08:00:00+00:00',
                '2026-06-11T08:00:00+00:00'
            )
            """,
            (str((path.parent / "belege" / "beleg_1.pdf").resolve()),),
        )
        connection.execute(
            """
            INSERT INTO vorgang_belege (
                vorgangs_id, beleg_id, erstellt_am
            ) VALUES (
                'vorgang_tx_newer', 'beleg_1',
                '2026-06-11T08:00:00+00:00'
            )
            """
        )
        connection.execute(
            """
            INSERT INTO budgets (
                saison, oberkategorie, unterkategorie, einnahmen, ausgaben
            ) VALUES ('2025/2026', 'Spielbetrieb', 'Eintritt', 100, 250)
            """
        )
        connection.commit()
    finally:
        connection.close()


class DashboardDataStoreTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = (
            Path(self.temporary_directory.name) / "transactions.sqlite3"
        )
        create_dashboard_database(self.database_path)
        self.store = DashboardDataStore(self.database_path)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _insert_opposite_transaction(self, transaction_id="tx_opposite"):
        with closing(connect_database(self.database_path)) as connection:
            connection.execute(
                """
                INSERT INTO transactions (
                    transaction_id, fingerprint, occurrence, provider,
                    account_id, account_name, account_number, booking_date,
                    value_date, counterparty, amount, currency, booking_text,
                    purpose, amount_minor, source_info, raw_fields_json,
                    first_seen_at, counterparty_account, creditor_id,
                    mandate_reference
                ) VALUES (
                    ?, ?, 1, 'testbank', 'acct_test', 'Hauptkonto', 'DE001',
                    '2026-06-11', '2026-06-11', 'Gegenbuchung', '-25.00',
                    'EUR', 'Ueberweisung', 'Ausgleich', -2500, 'Testquelle',
                    '{}', '2026-06-11T09:00:00+00:00', '', '', ''
                )
                """,
                (transaction_id, f"fp_{transaction_id}"),
            )
            connection.commit()

    def test_nullbuchung_groups_classifies_and_completes_two_transactions(self):
        self._insert_opposite_transaction()

        result = self.store.create_vorgang(
            {
                "title": "Ausgleich",
                "vorgangstyp": "Nullbuchung",
                "transaction_ids": ["tx_newer", "tx_opposite"],
            }
        )

        self.assertEqual("Nullbuchung", result["vorgangstyp"])
        self.assertEqual("abgeschlossen", result["status"])
        self.assertTrue(result["status_manuell"])
        self.assertEqual(
            ["tx_newer", "tx_opposite"],
            sorted(item["transaktions_id"] for item in result["transaktionen"]),
        )
        for transaction_id in ("tx_newer", "tx_opposite"):
            transaction = self.store.transaction_detail(transaction_id)
            self.assertEqual("Nullbuchung", transaction["transaktionstyp"])
            self.assertEqual("Sonstiges", transaction["oberkategorie"])
            self.assertEqual("Nullbuchung", transaction["unterkategorie"])
            self.assertEqual("Ideeller Bereich", transaction["sphaere"])

    def test_invalid_nullbuchung_leaves_transactions_unchanged(self):
        before = self.store.transaction_detail("tx_newer")

        with self.assertRaisesRegex(ValueError, "genau zwei"):
            self.store.create_vorgang(
                {
                    "vorgangstyp": "Nullbuchung",
                    "transaction_ids": ["tx_newer"],
                }
            )

        after = self.store.transaction_detail("tx_newer")
        self.assertEqual(before, after)

        with self.assertRaisesRegex(ValueError, "zusammen 0 EUR"):
            self.store.create_vorgang(
                {
                    "vorgangstyp": "Nullbuchung",
                    "transaction_ids": ["tx_newer", "tx_older"],
                }
            )

        self.assertEqual(before, self.store.transaction_detail("tx_newer"))
        self.assertEqual([], self.store.list_vorgaenge(search="Nullbuchung"))

    def _create_test_mail(
        self,
        inbox_id: str,
        *,
        is_read: bool = False,
        deleted: bool = False,
    ) -> None:
        InboxMailStore(self.database_path)
        now = "2026-06-11T08:00:00+00:00"
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                """
                INSERT INTO inbox_messages (
                    inbox_id, source, source_message_id, subject,
                    is_read, deleted_at, created_at, updated_at,
                    last_seen_at
                ) VALUES (?, 'test', ?, 'Testmail', ?, ?, ?, ?, ?)
                """,
                (
                    inbox_id,
                    inbox_id,
                    1 if is_read else 0,
                    now if deleted else None,
                    now,
                    now,
                    now,
                ),
            )
            connection.commit()

    def _link_test_mail_to_vorgang(
        self,
        inbox_id: str,
        vorgangs_id: str,
        *,
        is_read: bool = False,
        deleted: bool = False,
    ) -> None:
        self._create_test_mail(
            inbox_id,
            is_read=is_read,
            deleted=deleted,
        )
        now = "2026-06-11T08:00:00+00:00"
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                """
                INSERT INTO inbox_vorgaenge (
                    inbox_id, vorgangs_id, created_at
                ) VALUES (?, ?, ?)
                """,
                (inbox_id, vorgangs_id, now),
            )
            connection.commit()

    def _mail_is_read(self, inbox_id: str) -> bool:
        with closing(sqlite3.connect(self.database_path)) as connection:
            row = connection.execute(
                "SELECT is_read FROM inbox_messages WHERE inbox_id = ?",
                (inbox_id,),
            ).fetchone()
        return bool(row[0])

    def test_transactions_default_to_date_descending(self):
        rows = self.store.list_transactions()

        self.assertEqual(
            [row["transaktions_id"] for row in rows],
            ["tx_newer", "tx_older"],
        )

    def test_default_period_is_three_calendar_months(self):
        self.assertEqual(
            default_transaction_period(date(2026, 6, 11)),
            ("2026-03-11", "2026-06-11"),
        )

    def test_transactions_can_be_sorted_by_every_visible_column(self):
        for column in (
            "datum",
            "kontoname",
            "zahlungsbeteiligter",
            "verwendungszweck",
            "betrag",
        ):
            with self.subTest(column=column):
                self.assertEqual(
                    len(
                        self.store.list_transactions(
                            sort=column,
                            direction="asc",
                        )
                    ),
                    2,
                )

        amounts = self.store.list_transactions(
            sort="betrag",
            direction="asc",
        )
        self.assertEqual(amounts[0]["transaktions_id"], "tx_older")

    def test_search_covers_displayed_values_and_german_formats(self):
        self.assertEqual(
            self.store.list_transactions(search="älterer")[0][
                "transaktions_id"
            ],
            "tx_older",
        )
        self.assertEqual(
            self.store.list_transactions(search="10.06.2026")[0][
                "transaktions_id"
            ],
            "tx_newer",
        )
        self.assertEqual(
            self.store.list_transactions(search="12,34")[0][
                "transaktions_id"
            ],
            "tx_older",
        )
        self.assertEqual(
            self.store.list_transactions(search="25,00")[0][
                "transaktions_id"
            ],
            "tx_newer",
        )

    def test_transactions_can_be_filtered_by_period(self):
        rows = self.store.list_transactions(
            date_from="2026-06-01",
            date_to="2026-06-30",
        )

        self.assertEqual(
            [row["transaktions_id"] for row in rows],
            ["tx_newer"],
        )

    def test_transactions_can_be_filtered_to_unclassified_rows(self):
        with closing(connect_database(self.database_path)) as connection:
            connection.execute(
                """
                UPDATE transactions
                SET sub_category = ''
                WHERE transaction_id = 'tx_older'
                """
            )
            connection.commit()

        rows = self.store.list_transactions(unclassified_only=True)

        self.assertEqual(
            [row["transaktions_id"] for row in rows],
            ["tx_older"],
        )

    def test_transactions_can_hide_only_completed_vorgang_links(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                UPDATE vorgaenge
                SET status = 'abgeschlossen'
                WHERE vorgangs_id = 'vorgang_tx_older'
                """
            )
            connection.execute(
                """
                INSERT INTO vorgaenge (
                    vorgangs_id, titel, beschreibung, vorgangstyp,
                    status, erstellt_am, aktualisiert_am
                ) VALUES (
                    'vorgang_tx_newer_completed', '', '', 'Ausgabe',
                    'abgeschlossen', '2026-06-11T08:00:00+00:00',
                    '2026-06-11T08:00:00+00:00'
                )
                """
            )
            connection.execute(
                """
                INSERT INTO transaktion_vorgaenge (
                    transaktions_id, vorgangs_id
                ) VALUES ('tx_newer', 'vorgang_tx_newer_completed')
                """
            )
            connection.commit()
        finally:
            connection.close()

        unfiltered = self.store.list_transactions()
        filtered = self.store.list_transactions(
            hide_completed_vorgaenge=True,
        )

        self.assertEqual(
            [row["transaktions_id"] for row in unfiltered],
            ["tx_newer", "tx_older"],
        )
        newer = unfiltered[0]
        self.assertEqual(newer["vorgaenge_count"], 2)
        self.assertEqual(newer["completed_vorgaenge_count"], 1)
        self.assertTrue(newer["has_vorgaenge"])
        self.assertTrue(newer["has_completed_vorgaenge"])
        self.assertEqual(
            [row["transaktions_id"] for row in filtered],
            ["tx_newer"],
        )

    def test_transactions_without_vorgang_stay_visible_when_hiding_completed(
        self,
    ):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                DELETE FROM transaktion_vorgaenge
                WHERE transaktions_id = 'tx_older'
                """
            )
            connection.execute(
                """
                UPDATE vorgaenge
                SET status = 'abgeschlossen'
                WHERE vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.commit()
        finally:
            connection.close()

        rows = self.store.list_transactions(hide_completed_vorgaenge=True)

        self.assertEqual(
            [row["transaktions_id"] for row in rows],
            ["tx_older"],
        )

    def test_transaction_period_bounds_cover_database(self):
        bounds = self.store.transaction_period_bounds()

        self.assertTrue(bounds["available"])
        self.assertEqual(bounds["date_from"], "2026-05-10")
        self.assertEqual(bounds["date_to"], "2026-06-10")

    def test_link_candidate_catalog_lists_existing_entities(self):
        candidates = self.store.link_candidate_catalog()

        self.assertIn("transactions", candidates)
        self.assertIn(
            "tx_newer",
            [item["id"] for item in candidates["transactions"]],
        )
        transaction = next(
            item
            for item in candidates["transactions"]
            if item["id"] == "tx_newer"
        )
        self.assertTrue(transaction["classification_complete"])
        self.assertEqual([], transaction["classification_missing"])
        self.assertIn("classification", transaction)

    def test_balance_summary_reports_complete_total(self):
        summary = self.store.balance_summary()

        self.assertTrue(summary["vollstaendig"])
        self.assertEqual(summary["kontostand_gesamt"], "25.00")
        self.assertEqual(summary["konten"][0]["kontostand"], "25.00")

    def test_balance_history_contains_total_and_account_series(self):
        history = self.store.balance_history(
            date_from="2026-05-01",
            date_to="2026-06-10",
        )

        self.assertEqual(history["date_from"], "2026-05-01")
        self.assertEqual(history["series"][0]["id"], "gesamt")
        self.assertEqual(
            history["series"][0]["values"][-1]["value"],
            "25.00",
        )
        self.assertEqual(history["series"][1]["label"], "Hauptkonto")

    def test_detail_contains_links_sources_and_raw_fields(self):
        detail = self.store.transaction_detail("tx_newer")

        self.assertEqual(detail["vorgangs_ids"], ["vorgang_tx_newer"])
        self.assertNotIn("beleg_ids", detail)
        self.assertEqual(
            detail["splits"],
            [
                {
                    "split_id": "split_tx_newer_1",
                    "transaction_id": "tx_newer",
                    "transaktions_id": "tx_newer",
                    "sort_order": 0,
                    "reihenfolge": 0,
                    "amount_minor": 1500,
                    "betrag_cent": 1500,
                    "betrag": "15.00",
                    "description": "Teilbetrag Eintritt",
                    "beschreibung": "Teilbetrag Eintritt",
                    "transaction_type": "Einnahme",
                    "transaktionstyp": "Einnahme",
                    "top_category": "Spielbetrieb",
                    "oberkategorie": "Spielbetrieb",
                    "sub_category": "Eintritt",
                    "unterkategorie": "Eintritt",
                    "sphere": "Zweckbetrieb",
                    "sphaere": "Zweckbetrieb",
                    "professional_description": "Split-Test",
                    "fachliche_beschreibung": "Split-Test",
                    "klassifikationsstatus": "vollstaendig_klassifiziert",
                    "classification_status": "vollstaendig_klassifiziert",
                    "vorgangs_id": "vorgang_tx_newer",
                    "created_at": "2026-06-11T08:00:00+00:00",
                    "erstellt_am": "2026-06-11T08:00:00+00:00",
                    "updated_at": "2026-06-11T08:00:00+00:00",
                    "aktualisiert_am": "2026-06-11T08:00:00+00:00",
                }
            ],
        )
        self.assertEqual(detail["quellen"][0]["dateiname"], "test.csv")
        self.assertEqual(
            detail["rohdaten"]["Originalfeld"],
            "Weiterer Wert",
        )

    def test_detail_without_splits_returns_empty_split_list(self):
        detail = self.store.transaction_detail("tx_older")

        self.assertEqual(detail["splits"], [])

    def test_transaction_detail_includes_derived_split_classification_status(self):
        detail = self.store.transaction_detail("tx_newer")

        self.assertEqual(
            detail["splits"][0]["klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )
        self.assertEqual(
            detail["split_klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )
        self.assertEqual(
            detail["klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )
        self.assertEqual(
            detail["transaktions_klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )

        updated = self.store.replace_transaction_splits(
            "tx_newer",
            {
                "splits": [
                    {
                        "amount_minor": 1000,
                        "transaction_type": "Einnahme",
                        "top_category": "Spielbetrieb",
                        "sub_category": "Eintritt",
                        "sphere": "Zweckbetrieb",
                    },
                    {"amount_minor": 1500},
                ]
            },
        )["transaction"]

        self.assertEqual(
            [split["klassifikationsstatus"] for split in updated["splits"]],
            ["vollstaendig_klassifiziert", "unklassifiziert"],
        )
        self.assertEqual(
            updated["split_klassifikationsstatus"],
            "unvollstaendig_klassifiziert",
        )
        self.assertEqual(
            updated["gesamt_klassifikationsstatus"],
            "unvollstaendig_klassifiziert",
        )

    def test_split_responses_derive_each_classification_status(self):
        original = self.store.transaction_detail("tx_newer")
        original_classification = {
            field: original[field]
            for field in (
                "transaktionstyp",
                "oberkategorie",
                "unterkategorie",
                "sphaere",
                "fachliche_beschreibung",
                "klassifikationsstatus",
            )
        }

        response = self.store.replace_transaction_splits(
            "tx_newer",
            {
                "splits": [
                    {"amount_minor": 500},
                    {
                        "amount_minor": 500,
                        "transaction_type": "Einnahme",
                    },
                    {
                        "amount_minor": 500,
                        "professional_description": "Nur Beschreibung",
                    },
                    {
                        "amount_minor": 1000,
                        "transaction_type": "Einnahme",
                        "top_category": "Spielbetrieb",
                        "sub_category": "Eintritt",
                        "sphere": "Zweckbetrieb",
                    },
                ]
            },
        )

        expected_statuses = [
            "unklassifiziert",
            "unvollstaendig_klassifiziert",
            "unvollstaendig_klassifiziert",
            "vollstaendig_klassifiziert",
        ]
        self.assertEqual(
            [
                split["klassifikationsstatus"]
                for split in response["transaction"]["splits"]
            ],
            expected_statuses,
        )
        read_response = self.store.transaction_splits("tx_newer")
        self.assertEqual(
            [split["klassifikationsstatus"] for split in read_response["splits"]],
            expected_statuses,
        )
        self.assertEqual(
            {
                field: response["transaction"][field]
                for field in original_classification
            },
            original_classification,
        )

    def test_transaction_splits_can_be_replaced_with_valid_sum(self):
        result = self.store.replace_transaction_splits(
            "tx_newer",
            {
                    "splits": [
                        {
                            "amount_minor": 1000,
                            "description": "Teil 1",
                            "transaction_type": "Einnahme",
                            "top_category": "Spielbetrieb",
                            "sub_category": "Eintritt",
                            "sphere": "Zweckbetrieb",
                        },
                        {
                            "amount_minor": 1500,
                            "description": "Teil 2",
                            "transaction_type": "Einnahme",
                            "top_category": "Spielbetrieb",
                            "sub_category": "Eintritt",
                            "sphere": "Zweckbetrieb",
                            "vorgangs_id": "vorgang_tx_newer",
                        },
                    ]
            },
        )

        self.assertEqual(
            [split["betrag_cent"] for split in result["transaction"]["splits"]],
            [1000, 1500],
        )
        self.assertEqual(
            [split["amount_minor"] for split in result["transaction"]["splits"]],
            [1000, 1500],
        )
        self.assertEqual(
            [split["sort_order"] for split in result["transaction"]["splits"]],
            [1, 2],
        )
        self.assertEqual(
            self.store.transaction_detail("tx_newer")["splits"][1][
                "vorgangs_id"
            ],
            "vorgang_tx_newer",
        )

    def test_transaction_split_options_include_linked_vorgang_belege(self):
        response = self.store.transaction_splits("tx_newer")

        self.assertEqual(
            [item["vorgangs_id"] for item in response["zulaessige_vorgaenge"]],
            ["vorgang_tx_newer"],
        )
        self.assertEqual(
            response["zulaessige_vorgaenge"][0]["belege"],
            [
                {
                    "beleg_id": "beleg_1",
                    "dateiname": "beleg_1.pdf",
                    "kategorie": "sonstige_dokumente",
                    "dokumentdatum": "",
                    "betrag": "",
                }
            ],
        )

    def test_invalid_split_vorgang_keeps_existing_splits(self):
        original = self.store.transaction_splits("tx_newer")["splits"]

        for vorgangs_id, message in (
            ("vorgang_missing", "Unbekannte Vorgangs-ID"),
            (
                "vorgang_tx_older",
                "nicht mit dieser Transaktion verknuepft",
            ),
        ):
            with self.subTest(vorgangs_id=vorgangs_id):
                with self.assertRaisesRegex(ValueError, message):
                    self.store.replace_transaction_splits(
                        "tx_newer",
                        {
                            "splits": [
                                {
                                    "betrag_cent": 2500,
                                    "vorgangs_id": vorgangs_id,
                                }
                            ]
                        },
                    )
                self.assertEqual(
                    self.store.transaction_splits("tx_newer")["splits"],
                    original,
                )

    def test_split_classification_recalculates_automatic_vorgang_status(self):
        completed = self.store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": "Vergütung"},
        )
        self.assertEqual(completed["vorgaenge"][0]["status"], "abgeschlossen")

        incomplete = self.store.replace_transaction_splits(
            "tx_newer",
            {
                "splits": [
                    {
                        "amount_minor": 2500,
                        "transaction_type": "Einnahme",
                        "top_category": "Spielbetrieb",
                        "sub_category": "Eintritt",
                    }
                ]
            },
        )
        self.assertEqual(
            self.store.vorgang_detail("vorgang_tx_newer")["status"],
            "in_bearbeitung",
        )

        complete = self.store.replace_transaction_splits(
            "tx_newer",
            {
                "splits": [
                    {
                        "amount_minor": 2500,
                        "transaction_type": "Einnahme",
                        "top_category": "Spielbetrieb",
                        "sub_category": "Eintritt",
                        "sphere": "Zweckbetrieb",
                    }
                ]
            },
        )
        self.assertEqual(
            self.store.vorgang_detail("vorgang_tx_newer")["status"],
            "abgeschlossen",
        )

    def test_split_changes_preserve_manual_vorgang_status(self):
        self.store.update_vorgang_status("vorgang_tx_newer", True)

        response = self.store.replace_transaction_splits(
            "tx_newer",
            {"splits": [{"amount_minor": 2500}]},
        )

        vorgang = self.store.vorgang_detail("vorgang_tx_newer")
        self.assertEqual(vorgang["status"], "abgeschlossen")
        self.assertTrue(vorgang["status_manuell"])

    def test_transaction_splits_validate_negative_amounts(self):
        result = self.store.replace_transaction_splits(
            "tx_older",
            {
                "splits": [
                    {"betrag_cent": -1000, "beschreibung": "Ausgabe 1"},
                    {"betrag_cent": -234, "beschreibung": "Ausgabe 2"},
                ]
            },
        )

        self.assertEqual(
            [split["betrag_cent"] for split in result["transaction"]["splits"]],
            [-1000, -234],
        )

    def test_invalid_transaction_split_sum_keeps_existing_splits(self):
        with self.assertRaises(ValueError):
            self.store.replace_transaction_splits(
                "tx_newer",
                {"splits": [{"betrag_cent": 2400}]},
            )

        self.assertEqual(
            [split["split_id"] for split in self.store.transaction_detail(
                "tx_newer"
            )["splits"]],
            ["split_tx_newer_1"],
        )

    def test_invalid_split_sum_keeps_automatic_vorgang_status(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": "Vergütung"},
        )
        self.assertEqual(
            self.store.vorgang_detail("vorgang_tx_newer")["status"],
            "abgeschlossen",
        )

        with self.assertRaises(ValueError):
            self.store.replace_transaction_splits(
                "tx_newer",
                {"splits": [{"betrag_cent": 2499}]},
            )

        self.assertEqual(
            self.store.vorgang_detail("vorgang_tx_newer")["status"],
            "abgeschlossen",
        )
        self.assertEqual(
            [
                split["split_id"]
                for split in self.store.transaction_detail("tx_newer")["splits"]
            ],
            ["split_tx_newer_1"],
        )

    def test_invalid_transaction_split_payload_keeps_existing_splits(self):
        with self.assertRaises(ValueError):
            self.store.replace_transaction_splits(
                "tx_newer",
                {
                    "splits": [
                        {
                            "betrag_cent": 2500,
                            "transaction_id": "tx_older",
                        }
                    ]
                },
            )

        self.assertEqual(
            [split["split_id"] for split in self.store.transaction_detail(
                "tx_newer"
            )["splits"]],
            ["split_tx_newer_1"],
        )

        with self.assertRaises(ValueError):
            self.store.replace_transaction_splits(
                "tx_newer",
                {"splits": [{"betrag_cent": 2500, "unexpected": "x"}]},
            )

        self.assertEqual(
            [split["split_id"] for split in self.store.transaction_detail(
                "tx_newer"
            )["splits"]],
            ["split_tx_newer_1"],
        )

    def test_transaction_splits_can_be_removed(self):
        result = self.store.replace_transaction_splits(
            "tx_newer",
            {"splits": []},
        )

        self.assertEqual(result["transaction"]["splits"], [])

    def test_vorgang_detail_includes_transaction_splits(self):
        detail = self.store.vorgang_detail("vorgang_tx_newer")

        self.assertEqual(
            detail["transaktionen"][0]["splits"][0]["split_id"],
            "split_tx_newer_1",
        )

    def test_transaction_can_be_linked_to_existing_vorgang_idempotently(self):
        first = self.store.link_transaction_vorgang(
            "tx_newer",
            "vorgang_tx_older",
        )
        second = self.store.link_transaction_vorgang(
            "tx_newer",
            "vorgang_tx_older",
        )

        self.assertEqual(
            ["vorgang_tx_newer", "vorgang_tx_older"],
            sorted(first["transaction"]["vorgangs_ids"]),
        )
        self.assertEqual(
            ["vorgang_tx_newer", "vorgang_tx_older"],
            sorted(second["transaction"]["vorgangs_ids"]),
        )
        detail = self.store.vorgang_detail("vorgang_tx_older")
        self.assertEqual(
            ["tx_newer", "tx_older"],
            sorted(
                item["transaktions_id"]
                for item in detail["transaktionen"]
            ),
        )

    def test_transaction_link_rejects_unknown_vorgang(self):
        with self.assertRaisesRegex(LookupError, "Vorgang"):
            self.store.link_transaction_vorgang(
                "tx_newer",
                "vorgang_unbekannt",
            )

        self.assertEqual(
            ["vorgang_tx_newer"],
            self.store.transaction_detail("tx_newer")["vorgangs_ids"],
        )

    def test_transaction_suggestions_include_existing_vorgaenge(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                INSERT INTO vorgaenge (
                    vorgangs_id, titel, beschreibung, vorgangstyp,
                    status, erstellt_am, aktualisiert_am
                ) VALUES (
                    'vorgang_neuer_zweck', 'Neuer Zweck Sammelvorgang',
                    'Neuer Verein', 'Ausgabe', 'in_bearbeitung',
                    '2026-06-11T08:00:00+00:00',
                    '2026-06-11T08:00:00+00:00'
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

        result = self.store.suggest_related_entities(
            {"source_type": "transaction", "source_id": "tx_newer"}
        )

        self.assertIn("vorgaenge", result["suggestions"])
        self.assertIn("vorgaenge", result["candidates"])
        suggestion_ids = [
            item["id"] for item in result["suggestions"]["vorgaenge"]
        ]
        self.assertIn("vorgang_tx_newer", suggestion_ids)
        self.assertIn("vorgang_neuer_zweck", suggestion_ids)
        linked = next(
            item
            for item in result["suggestions"]["vorgaenge"]
            if item["id"] == "vorgang_tx_newer"
        )
        self.assertTrue(linked["selected"])

    def test_vorgaenge_are_listed_with_linked_transactions(self):
        rows = self.store.list_vorgaenge()
        detail = self.store.vorgang_detail("vorgang_tx_newer")

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["vorgangs_id"], "vorgang_tx_newer")
        self.assertEqual(rows[0]["status"], "in_bearbeitung")
        self.assertEqual(rows[0]["anzahl_transaktionen"], 1)
        self.assertEqual(detail["vorgangstyp"], "Ausgabe")
        self.assertEqual(
            detail["transaktionen"][0]["transaktions_id"],
            "tx_newer",
        )
        self.assertEqual(detail["belege"][0]["beleg_id"], "beleg_1")
        self.assertTrue(
            detail["belege"][0]["dateipfad"].endswith("beleg_1.pdf")
        )

    def test_completed_vorgaenge_can_be_hidden(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": "Vergütung"},
        )

        rows = self.store.list_vorgaenge(hide_completed=True)

        self.assertEqual(len(rows), 1)
        self.assertNotEqual(rows[0]["status"], "abgeschlossen")

    def test_vorgaenge_can_be_searched_and_completed_results_hidden(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                UPDATE vorgaenge
                SET status = 'abgeschlossen'
                WHERE vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.commit()
        finally:
            connection.close()

        rows = self.store.list_vorgaenge(search="Neuer Verein")
        hidden = self.store.list_vorgaenge(
            search="Neuer Verein",
            hide_completed=True,
        )
        empty = self.store.list_vorgaenge(search="Kein Treffer")

        self.assertEqual(
            [row["vorgangs_id"] for row in rows],
            ["vorgang_tx_newer"],
        )
        self.assertEqual(rows[0]["status"], "abgeschlossen")
        self.assertEqual(hidden, [])
        self.assertEqual(empty, [])

    def test_vorgaenge_prioritize_open_before_completed(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                UPDATE vorgaenge
                SET status = 'abgeschlossen',
                    aktualisiert_am = '2026-06-12T08:00:00+00:00'
                WHERE vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.commit()
        finally:
            connection.close()

        rows = self.store.list_vorgaenge()

        self.assertEqual(
            [row["vorgangs_id"] for row in rows],
            ["vorgang_tx_older", "vorgang_tx_newer"],
        )
        self.assertEqual(rows[0]["status"], "in_bearbeitung")
        self.assertEqual(rows[1]["status"], "abgeschlossen")

    def test_vorgaenge_search_prioritizes_open_before_completed(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                UPDATE vorgaenge
                SET status = 'abgeschlossen',
                    aktualisiert_am = '2026-06-12T08:00:00+00:00'
                WHERE vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.commit()
        finally:
            connection.close()

        rows = self.store.list_vorgaenge(search="Verein")
        hidden = self.store.list_vorgaenge(
            search="Verein",
            hide_completed=True,
        )

        self.assertEqual(
            [row["vorgangs_id"] for row in rows],
            ["vorgang_tx_older", "vorgang_tx_newer"],
        )
        self.assertEqual(
            [row["vorgangs_id"] for row in hidden],
            ["vorgang_tx_older"],
        )

    def test_classification_update_recalculates_both_statuses(self):
        completed = self.store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": "Vergütung"},
        )

        self.assertEqual(
            completed["transaction"]["klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )
        self.assertEqual(completed["vorgaenge"][0]["status"], "abgeschlossen")
        self.assertEqual(
            completed["vorgaenge"][0]["vorgangstyp"],
            "Ausgabe",
        )

        incomplete = self.store.update_transaction_classification(
            "tx_newer",
            {"sphaere": ""},
        )

        self.assertEqual(
            incomplete["transaction"]["klassifikationsstatus"],
            "unvollstaendig_klassifiziert",
        )
        self.assertEqual(
            incomplete["vorgaenge"][0]["status"],
            "in_bearbeitung",
        )

    def test_vorgang_status_can_be_set_manually_and_is_preserved(self):
        completed = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            True,
        )

        self.assertEqual(completed["status"], "abgeschlossen")
        self.assertTrue(completed["status_manuell"])

        classification = self.store.update_transaction_classification(
            "tx_newer",
            {"sphaere": ""},
        )
        self.assertEqual(
            classification["vorgaenge"][0]["status"],
            "in_bearbeitung",
        )
        self.assertTrue(classification["vorgaenge"][0]["status_manuell"])

        reopened = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            False,
        )
        self.assertEqual(reopened["status"], "in_bearbeitung")
        self.assertTrue(reopened["status_manuell"])

    def test_manual_vorgang_completion_marks_linked_mails_read(self):
        self._link_test_mail_to_vorgang(
            "mail_active",
            "vorgang_tx_newer",
        )
        self._link_test_mail_to_vorgang(
            "mail_deleted",
            "vorgang_tx_newer",
            deleted=True,
        )

        completed = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            True,
        )
        filtered = self.store.list_transactions(
            hide_completed_vorgaenge=True,
        )

        self.assertEqual(completed["status"], "abgeschlossen")
        self.assertTrue(self._mail_is_read("mail_active"))
        self.assertFalse(self._mail_is_read("mail_deleted"))
        self.assertEqual(
            [row["transaktions_id"] for row in filtered],
            ["tx_older"],
        )

        reopened = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            False,
        )

        self.assertEqual(reopened["status"], "in_bearbeitung")
        self.assertTrue(self._mail_is_read("mail_active"))

    def test_create_vorgang_marks_linked_mails_read(self):
        self._create_test_mail("mail_create_unread")
        self._create_test_mail("mail_create_read", is_read=True)

        created = self.store.create_vorgang(
            {
                "title": "Mailvorgang",
                "mail_ids": ["mail_create_unread", "mail_create_read"],
            }
        )

        self.assertTrue(created["vorgangs_id"].startswith("vorgang_"))
        self.assertCountEqual(
            ["mail_create_unread", "mail_create_read"],
            [mail["inbox_id"] for mail in created["mails"]],
        )
        self.assertTrue(self._mail_is_read("mail_create_unread"))
        self.assertTrue(self._mail_is_read("mail_create_read"))

    def test_update_vorgang_marks_newly_linked_mail_read(self):
        self._create_test_mail("mail_update_unread")

        updated = self.store.update_vorgang(
            "vorgang_tx_newer",
            {"mail_ids": ["mail_update_unread"]},
        )

        self.assertEqual(
            ["mail_update_unread"],
            [mail["inbox_id"] for mail in updated["mails"]],
        )
        self.assertTrue(self._mail_is_read("mail_update_unread"))

    def test_vorgang_cannot_be_completed_with_incomplete_transaction(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {"unterkategorie": ""},
        )

        with self.assertRaisesRegex(
            ValueError,
            "Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre",
        ):
            self.store.update_vorgang_status(
                "vorgang_tx_newer",
                True,
            )

        detail = self.store.vorgang_detail("vorgang_tx_newer")
        self.assertEqual(detail["status"], "in_bearbeitung")
        self.assertFalse(detail["abschluss_moeglich"])
        self.assertEqual(
            detail["unvollstaendige_transaktionen"],
            ["tx_newer"],
        )
        open_checks = [
            check
            for check in detail["abschluss_pruefung"]
            if check["status"] == "offen"
        ]
        self.assertEqual(1, len(open_checks))
        self.assertEqual("klassifikation", open_checks[0]["code"])
        self.assertIn("tx_newer", open_checks[0]["title"])
        self.assertIn("Unterkategorie", open_checks[0]["message"])
        self.assertNotIn("Oberkategorie", open_checks[0]["message"])

    def test_fehlbuchung_vorgang_can_be_completed_with_empty_sphere(self):
        self.store.update_vorgang(
            "vorgang_tx_newer",
            {
                "vorgangstyp": "Sonstige",
                "completed": False,
            },
        )
        self.store.update_transaction_classification(
            "tx_newer",
            {
                "oberkategorie": "Sonstige",
                "unterkategorie": "Fehlbuchung",
                "sphaere": "",
            },
        )

        detail = self.store.vorgang_detail("vorgang_tx_newer")
        self.assertTrue(detail["abschluss_moeglich"])
        self.assertEqual(detail["unvollstaendige_transaktionen"], [])

        completed = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            True,
        )

        self.assertEqual(completed["status"], "abgeschlossen")
        self.assertEqual(completed["transaktionen"][0]["sphaere"], "")

    def test_non_fehlbuchung_vorgang_still_requires_sphere(self):
        self.store.update_vorgang(
            "vorgang_tx_newer",
            {
                "vorgangstyp": "Sonstige",
                "completed": False,
            },
        )
        self.store.update_transaction_classification(
            "tx_newer",
            {
                "oberkategorie": "Sonstige",
                "unterkategorie": "Ausgleich",
                "sphaere": "",
            },
        )

        with self.assertRaisesRegex(ValueError, "Sph"):
            self.store.update_vorgang_status(
                "vorgang_tx_newer",
                True,
            )

        detail = self.store.vorgang_detail("vorgang_tx_newer")
        self.assertEqual(detail["status"], "in_bearbeitung")
        self.assertFalse(detail["abschluss_moeglich"])
        self.assertEqual(
            detail["unvollstaendige_transaktionen"],
            ["tx_newer"],
        )

    def test_rechnung_vorgang_requires_document_and_transaction_to_complete(self):
        updated = self.store.update_vorgang(
            "vorgang_tx_older",
            {
                "vorgangstyp": "Rechnung",
                "completed": False,
            },
        )
        self.assertFalse(updated["abschluss_moeglich"])
        self.assertIn("Dokument", " ".join(updated["abschluss_blocker"]))
        document_check = next(
            check
            for check in updated["abschluss_pruefung"]
            if check["code"] == "beleg"
        )
        self.assertEqual("offen", document_check["status"])
        self.assertEqual("Beleg fehlt", document_check["title"])
        self.assertIn("ordnen", document_check["action"].casefold())

        with self.assertRaisesRegex(ValueError, "Dokument"):
            self.store.update_vorgang_status("vorgang_tx_older", True)

        with self.assertRaisesRegex(ValueError, "Transaktion"):
            self.store.create_vorgang(
                {
                    "title": "Rechnung ohne Links",
                    "vorgangstyp": "Rechnung",
                    "completed": True,
                }
            )

    def test_rechnung_vorgang_can_complete_with_document_and_classified_transaction(self):
        updated = self.store.update_vorgang(
            "vorgang_tx_newer",
            {
                "vorgangstyp": "Rechnung",
                "completed": False,
                "transaction_ids": ["tx_newer"],
                "beleg_ids": ["beleg_1"],
            },
        )

        self.assertTrue(updated["abschluss_moeglich"])
        self.assertTrue(updated["abschluss_pruefung"])
        self.assertTrue(all(
            check["status"] == "erfuellt"
            for check in updated["abschluss_pruefung"]
        ))

        completed = self.store.update_vorgang_status(
            "vorgang_tx_newer",
            True,
        )

        self.assertEqual("abgeschlossen", completed["status"])

    def test_rechnung_completion_checklists_all_open_blockers(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {"oberkategorie": "", "sphaere": ""},
        )
        detail = self.store.update_vorgang(
            "vorgang_tx_newer",
            {
                "vorgangstyp": "Rechnung",
                "completed": False,
                "transaction_ids": ["tx_newer"],
                "beleg_ids": [],
            },
        )

        open_checks = [
            check
            for check in detail["abschluss_pruefung"]
            if check["status"] == "offen"
        ]
        self.assertEqual(
            ["klassifikation", "beleg"],
            [check["code"] for check in open_checks],
        )
        self.assertIn("Oberkategorie", open_checks[0]["message"])
        self.assertIn("Sphäre", open_checks[0]["message"])

    def test_incomplete_transaction_reopens_every_linked_vorgang(self):
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                """
                INSERT INTO transaktion_vorgaenge (
                    transaktions_id, vorgangs_id
                ) VALUES ('tx_newer', 'vorgang_tx_older')
                """
            )
            connection.commit()
        finally:
            connection.close()
        completed = self.store.update_vorgang_status(
            "vorgang_tx_older",
            True,
        )
        self.assertEqual(completed["status"], "abgeschlossen")

        result = self.store.update_transaction_classification(
            "tx_newer",
            {"sphaere": ""},
        )

        statuses = {
            vorgang["vorgangs_id"]: vorgang["status"]
            for vorgang in result["vorgaenge"]
        }
        self.assertEqual(statuses["vorgang_tx_newer"], "in_bearbeitung")
        self.assertEqual(statuses["vorgang_tx_older"], "in_bearbeitung")

    def test_linking_incomplete_transaction_reopens_completed_vorgang(self):
        completed = self.store.update_vorgang_status(
            "vorgang_tx_older",
            True,
        )
        self.assertEqual(completed["status"], "abgeschlossen")
        self.store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": ""},
        )

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                """
                INSERT INTO transaktion_vorgaenge (
                    transaktions_id, vorgangs_id
                ) VALUES ('tx_newer', 'vorgang_tx_older')
                """
            )
            connection.commit()
        finally:
            connection.close()

        detail = self.store.vorgang_detail("vorgang_tx_older")
        self.assertEqual(detail["status"], "in_bearbeitung")
        self.assertFalse(detail["abschluss_moeglich"])

    def test_vorgang_status_rejects_non_boolean_values(self):
        with self.assertRaises(ValueError):
            self.store.update_vorgang_status(
                "vorgang_tx_newer",
                "yes",
            )

    def test_classification_update_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            self.store.update_transaction_classification(
                "tx_newer",
                {"transaction_id": "manipuliert"},
            )

    def test_rules_can_be_listed_created_and_applied(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {
                "transaktionstyp": "",
                "oberkategorie": "",
                "unterkategorie": "",
                "sphaere": "",
                "fachliche_beschreibung": "",
            },
        )
        result = self.store.create_rule(
            {
                "name": "Neuer-Zweck-Regel",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "contains",
                "match_value": "Neuer Zweck",
                "transaction_type": "Einnahme",
                "top_category": "Test",
                "sub_category": "Dashboard",
                "sphere": "Ideeller Bereich",
                "professional_description": "Automatisch klassifiziert",
                "apply_now": True,
            }
        )

        self.assertEqual(result["changed_transactions"], 1)
        rules = self.store.list_rules()
        self.assertIn(
            "Neuer-Zweck-Regel",
            [rule["name"] for rule in rules["rules"]],
        )
        detail = self.store.transaction_detail("tx_newer")
        self.assertEqual(detail["transaktionstyp"], "Einnahme")

    def test_rules_can_be_searched_and_updated(self):
        created = self.store.create_rule(
            {
                "name": "Suchbare Regel",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "contains",
                "match_value": "Nicht vorhanden",
                "transaction_type": "Ausgabe",
                "top_category": "Alt",
                "sub_category": "Alt",
                "sphere": "Ideeller Bereich",
                "professional_description": "Alter Wert",
                "apply_now": False,
            }
        )
        rule_id = created["rule"]["rule_id"]

        updated = self.store.update_rule(
            rule_id,
            {
                "name": "Suchbare Regel geändert",
                "enabled": False,
                "match_field": "counterparty",
                "match_operator": "equals",
                "match_value": "Neuer Verein",
                "transaction_type": "Einnahme",
                "top_category": "Neu",
                "sub_category": "Bearbeitet",
                "sphere": "Zweckbetrieb",
                "professional_description": "Neuer Wert",
                "apply_now": False,
            },
        )

        self.assertEqual(updated["rule"]["rule_id"], rule_id)
        self.assertFalse(updated["rule"]["enabled"])
        search = self.store.list_rules(search="bearbeitet")
        self.assertEqual(
            [rule["rule_id"] for rule in search["rules"]],
            [rule_id],
        )

    def test_completion_rules_run_after_classification_rules(self):
        self.store.update_transaction_classification(
            "tx_newer",
            {
                "transaktionstyp": "",
                "oberkategorie": "",
                "unterkategorie": "",
                "sphaere": "",
                "fachliche_beschreibung": "",
            },
        )
        self.store.create_completion_rule(
            {
                "name": "Testklassifikation abschließen",
                "enabled": True,
                "match_field": "top_category",
                "match_operator": "equals",
                "match_value": "Automatik",
                "apply_now": False,
            }
        )

        result = self.store.create_rule(
            {
                "name": "Erst klassifizieren",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "equals",
                "match_value": "Neuer Zweck",
                "transaction_type": "Ausgabe",
                "top_category": "Automatik",
                "sub_category": "Test",
                "sphere": "Ideeller Bereich",
                "professional_description": "",
                "apply_now": True,
            }
        )

        self.assertEqual(result["changed_transactions"], 1)
        self.assertEqual(result["changed_vorgaenge"], 1)
        detail = self.store.vorgang_detail("vorgang_tx_newer")
        self.assertEqual(detail["status"], "abgeschlossen")
        self.assertFalse(detail["status_manuell"])

    def test_manual_classification_applies_completion_rules(self):
        self.store.create_completion_rule(
            {
                "name": "Spielbetrieb abschließen",
                "enabled": True,
                "conditions": [
                    {
                        "connector": "",
                        "match_field": "top_category",
                        "match_operator": "equals",
                        "match_value": "Automatisch",
                    },
                    {
                        "connector": "and",
                        "match_field": "sphere",
                        "match_operator": "equals",
                        "match_value": "Zweckbetrieb",
                    },
                ],
                "apply_now": False,
            }
        )

        result = self.store.update_transaction_classification(
            "tx_newer",
            {"oberkategorie": "Automatisch"},
        )

        self.assertEqual(
            result["vorgaenge"][0]["status"],
            "abgeschlossen",
        )
        self.assertFalse(result["vorgaenge"][0]["status_manuell"])

        reopened = self.store.update_transaction_classification(
            "tx_newer",
            {"unterkategorie": ""},
        )
        self.assertEqual(
            reopened["vorgaenge"][0]["status"],
            "in_bearbeitung",
        )

    def test_manual_classification_completion_marks_linked_mails_read(self):
        self.store.create_completion_rule(
            {
                "name": "Spielbetrieb abschlieÃŸen",
                "enabled": True,
                "conditions": [
                    {
                        "connector": "",
                        "match_field": "top_category",
                        "match_operator": "equals",
                        "match_value": "Automatisch",
                    },
                    {
                        "connector": "and",
                        "match_field": "sphere",
                        "match_operator": "equals",
                        "match_value": "Zweckbetrieb",
                    },
                ],
                "apply_now": False,
            }
        )
        self._link_test_mail_to_vorgang(
            "mail_rule",
            "vorgang_tx_newer",
        )

        result = self.store.update_transaction_classification(
            "tx_newer",
            {"oberkategorie": "Automatisch"},
        )
        filtered = self.store.list_transactions(
            hide_completed_vorgaenge=True,
        )

        self.assertEqual(
            result["vorgaenge"][0]["status"],
            "abgeschlossen",
        )
        self.assertTrue(self._mail_is_read("mail_rule"))
        self.assertEqual(
            [row["transaktions_id"] for row in filtered],
            ["tx_older"],
        )

    def test_completion_rules_create_completed_standard_vorgang(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                DELETE FROM transaktion_vorgaenge
                WHERE transaktions_id = 'tx_newer'
                """
            )
            connection.execute(
                """
                DELETE FROM vorgaenge
                WHERE vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.commit()
        finally:
            connection.close()

        self.store.create_completion_rule(
            {
                "name": "Alle Ausgaben abschliessen",
                "enabled": True,
                "match_field": "transaction_type",
                "match_operator": "equals",
                "match_value": "Ausgabe",
                "apply_now": False,
            }
        )

        result = self.store.update_transaction_classification(
            "tx_newer",
            {"fachliche_beschreibung": "Automatisch abgeschlossen"},
        )

        self.assertEqual(
            [vorgang["vorgangs_id"] for vorgang in result["vorgaenge"]],
            ["vorgang_tx_newer"],
        )
        self.assertEqual(result["vorgaenge"][0]["status"], "abgeschlossen")
        self.assertFalse(result["vorgaenge"][0]["status_manuell"])

    def test_completion_rules_do_not_override_manual_status(self):
        self.store.create_completion_rule(
            {
                "name": "Alle Ausgaben abschließen",
                "enabled": True,
                "match_field": "transaction_type",
                "match_operator": "equals",
                "match_value": "Ausgabe",
                "apply_now": False,
            }
        )
        self.store.update_vorgang_status("vorgang_tx_newer", False)

        result = self.store.update_transaction_classification(
            "tx_newer",
            {"fachliche_beschreibung": "Manuell geändert"},
        )

        self.assertEqual(
            result["vorgaenge"][0]["status"],
            "in_bearbeitung",
        )
        self.assertTrue(result["vorgaenge"][0]["status_manuell"])

    def test_completion_rules_can_be_listed_updated_and_deleted(self):
        created = self.store.create_completion_rule(
            {
                "name": "Temporäre Abschlussregel",
                "enabled": True,
                "match_field": "sub_category",
                "match_operator": "equals",
                "match_value": "Eintritt",
                "apply_now": True,
            }
        )
        rule_id = created["rule"]["rule_id"]
        self.assertGreaterEqual(created["changed_vorgaenge"], 1)

        listed = self.store.list_completion_rules("Tempor")
        self.assertEqual(
            [rule["rule_id"] for rule in listed["rules"]],
            [rule_id],
        )

        updated = self.store.update_completion_rule(
            rule_id,
            {
                "name": "Deaktivierte Abschlussregel",
                "enabled": False,
                "match_field": "sub_category",
                "match_operator": "equals",
                "match_value": "Eintritt",
                "apply_now": True,
            },
        )
        self.assertFalse(updated["rule"]["enabled"])
        self.assertEqual(
            self.store.vorgang_detail("vorgang_tx_newer")["status"],
            "in_bearbeitung",
        )

        deleted = self.store.delete_completion_rule(rule_id)
        self.assertEqual(deleted["deleted_rule_id"], rule_id)

    def test_classification_options_include_history_and_preferred_sphere(self):
        connection = connect_database(self.database_path)
        try:
            connection.execute(
                """
                UPDATE transactions
                SET
                    transaction_type = 'Mitgliedsbeitrag',
                    top_category = 'Mitglieder',
                    sub_category = 'Jahresbeitrag',
                    sphere = 'Zweckbetrieb'
                WHERE transaction_id IN ('tx_older', 'tx_newer')
                """
            )
            connection.commit()
        finally:
            connection.close()
        self.store.create_rule(
            {
                "name": "Abweichende Sphäre",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "contains",
                "match_value": "Kein Treffer",
                "transaction_type": "Sondertyp",
                "top_category": "Mitglieder",
                "sub_category": "Jahresbeitrag",
                "sphere": "Ideeller Bereich",
                "professional_description": "",
                "apply_now": False,
            }
        )

        options = self.store.classification_options()

        self.assertIn("Mitgliedsbeitrag", options["transaction_types"])
        self.assertIn("Sondertyp", options["transaction_types"])
        self.assertIn("Mitglieder", options["top_categories"])
        subcategories = {
            entry["top_category"]: entry["values"]
            for entry in options["sub_categories"]
        }
        self.assertIn("Jahresbeitrag", subcategories["Mitglieder"])
        defaults = {
            (entry["top_category"], entry["sub_category"]): entry["sphere"]
            for entry in options["sphere_defaults"]
        }
        self.assertEqual(
            defaults[("Mitglieder", "Jahresbeitrag")],
            "Zweckbetrieb",
        )
        self.assertEqual(
            options["spheres"],
            [
                "Ideeller Bereich",
                "Zweckbetrieb",
                "Wirtschaftlicher Geschäftsbetrieb",
                "Vermögensverwaltung",
            ],
        )

    def test_rule_can_be_deleted_permanently(self):
        created = self.store.create_rule(
            {
                "name": "Zu entfernende Regel",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "contains",
                "match_value": "Entfernen",
                "transaction_type": "Ausgabe",
                "top_category": "Test",
                "sub_category": "Loeschen",
                "sphere": "Ideeller Bereich",
                "professional_description": "",
                "apply_now": False,
            }
        )
        rule_id = created["rule"]["rule_id"]

        result = self.store.delete_rule(rule_id)

        self.assertEqual(result["deleted_rule_id"], rule_id)
        self.assertNotIn(
            rule_id,
            [
                rule["rule_id"]
                for rule in self.store.list_rules()["rules"]
            ],
        )
        with self.assertRaises(LookupError):
            self.store.delete_rule(rule_id)

    def test_default_rule_stays_deleted(self):
        default_rule_id = self.store.list_rules()["rules"][0]["rule_id"]

        self.store.delete_rule(default_rule_id)

        self.assertNotIn(
            default_rule_id,
            [
                rule["rule_id"]
                for rule in self.store.list_rules()["rules"]
            ],
        )

    def test_rule_can_be_created_without_professional_description(self):
        result = self.store.create_rule(
            {
                "name": "Regel ohne Beschreibung",
                "enabled": True,
                "match_field": "purpose",
                "match_operator": "contains",
                "match_value": "Optional",
                "transaction_type": "Ausgabe",
                "top_category": "Test",
                "sub_category": "Optional",
                "sphere": "Ideeller Bereich",
                "apply_now": False,
            }
        )

        self.assertEqual(
            result["rule"]["professional_description"],
            "",
        )

    def test_rule_supports_multiple_conditions_and_exclusions(self):
        for transaction_id in ("tx_older", "tx_newer"):
            self.store.update_transaction_classification(
                transaction_id,
                {
                    "transaktionstyp": "",
                    "oberkategorie": "",
                    "unterkategorie": "",
                    "sphaere": "",
                    "fachliche_beschreibung": "",
                },
            )

        result = self.store.create_rule(
            {
                "name": "Mehrere Bedingungen",
                "enabled": True,
                "conditions": [
                    {
                        "connector": "",
                        "match_field": "purpose",
                        "match_operator": "contains",
                        "match_value": "Zweck",
                    },
                    {
                        "connector": "and_not",
                        "match_field": "counterparty",
                        "match_operator": "equals",
                        "match_value": "Neuer Verein",
                    },
                ],
                "transaction_type": "Einnahme",
                "top_category": "Test",
                "sub_category": "Mehrfach",
                "sphere": "Ideeller Bereich",
                "professional_description": "",
                "apply_now": True,
            }
        )

        self.assertEqual(result["changed_transactions"], 1)
        self.assertEqual(
            result["rule"]["conditions"][1]["connector"],
            "and_not",
        )
        self.assertEqual(
            self.store.transaction_detail("tx_older")["transaktionstyp"],
            "Einnahme",
        )
        self.assertEqual(
            self.store.transaction_detail("tx_newer")["transaktionstyp"],
            "",
        )
        self.assertEqual(
            len(self.store.list_rules(search="OHNE")["rules"]),
            1,
        )

    def test_and_conditions_are_evaluated_before_or_conditions(self):
        for transaction_id in ("tx_older", "tx_newer"):
            self.store.update_transaction_classification(
                transaction_id,
                {
                    "transaktionstyp": "",
                    "oberkategorie": "",
                    "unterkategorie": "",
                    "sphaere": "",
                    "fachliche_beschreibung": "",
                },
            )

        result = self.store.create_rule(
            {
                "name": "Operatorrangfolge",
                "enabled": True,
                "conditions": [
                    {
                        "connector": "",
                        "match_field": "amount",
                        "match_operator": "equals",
                        "match_value": "-12.34",
                    },
                    {
                        "connector": "or",
                        "match_field": "purpose",
                        "match_operator": "equals",
                        "match_value": "Neuer Zweck",
                    },
                    {
                        "connector": "and",
                        "match_field": "amount",
                        "match_operator": "equals",
                        "match_value": "25.00",
                    },
                ],
                "transaction_type": "Einnahme",
                "top_category": "Test",
                "sub_category": "Rangfolge",
                "sphere": "Ideeller Bereich",
                "professional_description": "",
                "apply_now": True,
            }
        )

        self.assertEqual(result["changed_transactions"], 2)

    def test_invalid_condition_logic_is_rejected(self):
        base = {
            "name": "UngÃ¼ltige Logik",
            "enabled": True,
            "transaction_type": "Einnahme",
            "top_category": "Test",
            "sub_category": "Logik",
            "sphere": "Ideeller Bereich",
            "professional_description": "",
            "apply_now": False,
        }
        condition = {
            "match_field": "purpose",
            "match_operator": "contains",
            "match_value": "Test",
        }
        invalid_conditions = (
            [
                {"connector": "", **condition},
                {"connector": "and_not", **condition},
            ],
            [
                {"connector": "", **condition},
                {"connector": "or_not", **condition},
                {
                    "connector": "or",
                    "match_field": "counterparty",
                    "match_operator": "equals",
                    "match_value": "Verein",
                },
            ],
        )

        for conditions in invalid_conditions:
            with self.subTest(conditions=conditions):
                with self.assertRaises(ValueError):
                    self.store.create_rule(
                        {**base, "conditions": conditions}
                    )

    def test_version_one_rule_database_is_migrated(self):
        path = Path(self.temporary_directory.name) / "legacy-rules.sqlite3"
        connection = sqlite3.connect(path)
        try:
            connection.executescript(
                """
                CREATE TABLE schema_info (version INTEGER NOT NULL);
                INSERT INTO schema_info(version) VALUES (1);
                CREATE TABLE classification_rules (
                    rule_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    enabled INTEGER NOT NULL,
                    match_field TEXT NOT NULL,
                    match_operator TEXT NOT NULL,
                    match_value TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    top_category TEXT NOT NULL,
                    sub_category TEXT NOT NULL,
                    sphere TEXT NOT NULL,
                    professional_description TEXT NOT NULL
                );
                INSERT INTO classification_rules VALUES (
                    'legacy', 'Alte Regel', 1, 'purpose', 'contains',
                    'Alt', 'Ausgabe', 'Test', 'Migration',
                    'Ideeller Bereich', ''
                );
                """
            )
            connection.commit()
        finally:
            connection.close()

        migrated = connect_rules_database(path)
        try:
            rules = {
                rule.rule_id: rule
                for rule in list_classification_rules(migrated)
            }
            version = migrated.execute(
                "SELECT version FROM schema_info"
            ).fetchone()[0]
        finally:
            migrated.close()

        self.assertEqual(version, 3)
        self.assertEqual(len(rules["legacy"].conditions), 1)
        self.assertEqual(
            rules["legacy"].conditions[0].match_value,
            "Alt",
        )
        completion_connection = connect_rules_database(path)
        try:
            completion_rules = list_completion_rules(
                completion_connection
            )
        finally:
            completion_connection.close()
        self.assertEqual(
            completion_rules[0].name,
            "Vergütungen automatisch abschließen",
        )

    def test_budget_rows_are_available(self):
        budgets = self.store.list_budgets()

        self.assertEqual(len(budgets), 1)
        self.assertEqual(budgets[0]["budget"], 150)

    def test_todos_can_be_created_linked_updated_and_deleted(self):
        todo = self.store.create_todo(
            {
                "title": "Rechnung prüfen",
                "description": "Beleg und Betrag abgleichen.",
                "due_date": "2026-06-30",
                "priority": "hoch",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )

        self.assertTrue(todo["todo_id"].startswith("todo_"))
        self.assertEqual("manual", todo["source"])
        self.assertEqual(["vorgang_tx_newer"], todo["vorgangs_ids"])
        self.assertEqual(
            todo["todo_id"],
            self.store.vorgang_detail("vorgang_tx_newer")["todos"][0][
                "todo_id"
            ],
        )

        updated = self.store.update_todo(
            todo["todo_id"],
            {"completed": True, "priority": "normal"},
        )
        self.assertTrue(updated["completed"])
        self.assertIsNotNone(updated["completed_at"])
        self.assertEqual("normal", updated["priority"])

        deleted = self.store.delete_todo(todo["todo_id"])
        self.assertTrue(deleted["deleted"])
        self.assertEqual([], self.store.list_todos())

    def test_automatic_todo_source_is_available_for_later_integrations(self):
        todo = self.store.create_todo(
            {
                "title": "Mail beantworten",
                "vorgangs_ids": [],
            },
            source="automatic",
            source_reference="inbox_test",
        )

        self.assertEqual("automatic", todo["source"])
        self.assertEqual("inbox_test", todo["source_reference"])

    def test_todo_creation_with_unknown_vorgang_is_atomic(self):
        with self.assertRaises(LookupError):
            self.store.create_todo(
                {
                    "title": "Ungültige Zuordnung",
                    "vorgangs_ids": ["vorgang_fehlend"],
                }
            )

        self.assertEqual([], self.store.list_todos())

    def test_belege_directory_is_catalogued_and_linked_to_vorgang(self):
        belege_directory = self.database_path.parent / "belege"
        belege_directory.mkdir(exist_ok=True)
        document_path = belege_directory / "rechnung.pdf"
        document_path.write_bytes(b"%PDF-test")
        store = DashboardDataStore(self.database_path)

        belege = store.list_belege()
        document = next(
            item for item in belege if item["dateiname"] == "rechnung.pdf"
        )
        linked = store.link_beleg_vorgang(
            document["beleg_id"],
            "vorgang_tx_newer",
        )

        self.assertEqual(str(document_path.resolve()), document["dateipfad"])
        self.assertTrue(document["vorhanden"])
        self.assertEqual(9, document["dateigroesse"])
        self.assertEqual(
            ["vorgang_tx_newer"],
            linked["vorgangs_ids"],
        )
        self.assertIn(
            document["beleg_id"],
            [
                item["beleg_id"]
                for item in store.vorgang_detail(
                    "vorgang_tx_newer"
                )["belege"]
            ],
        )

    def test_overview_counts_cover_unassigned_entities(self):
        todo = self.store.create_todo({"title": "Offene Aufgabe"})
        self.store.create_termin(
            {
                "title": "Mitgliederversammlung",
                "starts_at": "2999-01-15T18:00:00+01:00",
            }
        )
        inbox_store = InboxMailStore(self.database_path)
        inbox_store.upsert_overview(
            {
                "source": "graph",
                "id": "unlinked-mail",
                "subject": "Ungelesen",
                "folderName": "Posteingang",
                "receivedDateTime": "2026-06-20T10:00:00+00:00",
                "isRead": False,
            }
        )
        inbox_store.upsert_overview(
            {
                "source": "graph",
                "id": "archive-mail",
                "subject": "Archiv",
                "folderName": "Archiv",
                "receivedDateTime": "2026-06-20T08:00:00+00:00",
                "isRead": False,
            }
        )
        inbox_store.upsert_overview(
            {
                "source": "graph",
                "id": "read-mail",
                "subject": "Gelesen",
                "folderName": "Junk-E-Mail",
                "receivedDateTime": "2026-06-20T07:00:00+00:00",
                "isRead": True,
            }
        )

        overview = self.store.overview_counts()

        self.assertEqual(2, overview["counts"]["open_vorgaenge"])
        self.assertEqual(1, overview["counts"]["unread_mails"])
        self.assertEqual(0, overview["counts"]["unclassified_transactions"])
        self.assertNotIn("unassigned_mails", overview["counts"])
        self.assertNotIn(
            "unassigned_mails",
            {card["key"] for card in overview["cards"]},
        )
        self.assertEqual(0, overview["counts"]["unassigned_transactions"])
        self.assertEqual(0, overview["counts"]["unassigned_documents"])
        self.assertEqual(1, overview["counts"]["open_todos"])
        self.assertEqual(1, overview["counts"]["upcoming_termine"])
        self.assertEqual(1, overview["counts"]["unassigned_termine"])
        self.assertEqual(
            {"open_vorgaenge", "open_todos", "upcoming_termine"},
            set(overview["previews"]),
        )
        self.assertEqual(
            "Offene Aufgabe",
            overview["previews"]["open_todos"][0]["title"],
        )
        self.assertEqual(
            "Mitgliederversammlung",
            overview["previews"]["upcoming_termine"][0]["title"],
        )
        self.assertLessEqual(len(overview["previews"]["open_vorgaenge"]), 5)
        self.assertEqual(
            list(range(1, 8)),
            [card["priority"] for card in overview["cards"]],
        )
        self.assertEqual(
            "unclassified_transactions",
            overview["cards"][0]["key"],
        )
        self.assertEqual("empty", overview["cards"][0]["state"])
        self.assertEqual("open", overview["cards"][1]["state"])
        document_card = next(
            card
            for card in overview["cards"]
            if card["key"] == "unassigned_documents"
        )
        self.assertEqual("documents", document_card["entity"])
        self.assertEqual(todo["todo_id"], self.store.list_todos()[0]["todo_id"])

    def test_overview_counts_incomplete_transactions_as_unclassified(self):
        with closing(sqlite3.connect(self.database_path)) as connection:
            cursor = connection.execute(
                """
                UPDATE transaction_splits
                SET sub_category = ''
                WHERE transaction_id = 'tx_newer'
                """
            )
            if cursor.rowcount == 0:
                connection.execute(
                    """
                    UPDATE transactions
                    SET sub_category = ''
                    WHERE transaction_id = 'tx_newer'
                    """
                )
            connection.commit()

        overview = self.store.overview_counts()

        self.assertEqual(1, overview["counts"]["unclassified_transactions"])
        transaction_card = overview["cards"][0]
        self.assertEqual("unclassified_transactions", transaction_card["key"])
        self.assertEqual(1, transaction_card["count"])
        self.assertEqual("open", transaction_card["state"])
        self.assertEqual("1 offen", transaction_card["state_label"])

    def test_overview_counts_only_relevant_open_upcoming_termine(self):
        self.store.create_termin(
            {
                "title": "Geplanter Zukunftstermin",
                "starts_at": "2999-01-15T18:00:00+01:00",
            }
        )
        self.store.create_termin(
            {
                "title": "Geplanter Datumstermin",
                "starts_at": "2999-01-16",
            }
        )
        self.store.create_termin(
            {
                "title": "Geplanter Vergangenheitstermin",
                "starts_at": "2000-01-15T18:00:00+01:00",
            }
        )
        self.store.create_termin(
            {
                "title": "Abgeschlossener Zukunftstermin",
                "starts_at": "2999-01-17T18:00:00+01:00",
                "status": TERMIN_STATUS_COMPLETED,
            }
        )
        self.store.create_termin(
            {
                "title": "Abgesagter Zukunftstermin",
                "starts_at": "2999-01-18T18:00:00+01:00",
                "status": TERMIN_STATUS_CANCELLED,
            }
        )
        self.store.create_termin(
            {
                "title": "Verknuepfter Zukunftstermin",
                "starts_at": "2999-01-19T18:00:00+01:00",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )

        overview = self.store.overview_counts()

        self.assertEqual(3, overview["counts"]["upcoming_termine"])
        self.assertEqual(2, overview["counts"]["unassigned_termine"])
        unassigned_card = next(
            card
            for card in overview["cards"]
            if card["key"] == "unassigned_termine"
        )
        self.assertEqual(
            "Nicht zugewiesene anstehende Termine",
            unassigned_card["label"],
        )

    def test_today_termine_treat_iso_date_and_timestamp_as_upcoming_day(self):
        today = date.today()
        today_date = today.isoformat()
        yesterday_timestamp = (
            today - timedelta(days=1)
        ).isoformat() + "T23:59:59"
        date_termin = self.store.create_termin(
            {
                "title": "Heutiger Datumstermin",
                "starts_at": today_date,
            }
        )
        timestamp_termin = self.store.create_termin(
            {
                "title": "Heutiger Zeitstempeltermin",
                "starts_at": today_date + "T00:00:00",
            }
        )
        self.store.create_termin(
            {
                "title": "Gestriger Zeitstempeltermin",
                "starts_at": yesterday_timestamp,
            }
        )

        overview = self.store.overview_counts()
        termine = self.store.list_termine(unassigned_upcoming=True)

        self.assertEqual(2, overview["counts"]["upcoming_termine"])
        self.assertEqual(2, overview["counts"]["unassigned_termine"])
        self.assertEqual(
            [date_termin["termin_id"], timestamp_termin["termin_id"]],
            [termin["termin_id"] for termin in termine],
        )
        self.assertEqual(today_date, termine[0]["starts_at"])
        self.assertEqual(today_date + "T00:00:00", termine[1]["starts_at"])

    def test_list_termine_filters_unassigned_upcoming_termine(self):
        expected = self.store.create_termin(
            {
                "title": "Unzugewiesener Zukunftstermin",
                "starts_at": "2999-01-15T18:00:00+01:00",
            }
        )
        self.store.create_termin(
            {
                "title": "Verknuepfter Zukunftstermin",
                "starts_at": "2999-01-16T18:00:00+01:00",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )
        self.store.create_termin(
            {
                "title": "Vergangener Termin",
                "starts_at": "2000-01-15T18:00:00+01:00",
            }
        )
        self.store.create_termin(
            {
                "title": "Abgeschlossener Zukunftstermin",
                "starts_at": "2999-01-17T18:00:00+01:00",
                "status": TERMIN_STATUS_COMPLETED,
            }
        )
        self.store.create_termin(
            {
                "title": "Abgesagter Zukunftstermin",
                "starts_at": "2999-01-18T18:00:00+01:00",
                "status": TERMIN_STATUS_CANCELLED,
            }
        )

        termine = self.store.list_termine(unassigned_upcoming=True)

        self.assertEqual(
            [expected["termin_id"]],
            [termin["termin_id"] for termin in termine],
        )

    def test_vorgang_can_be_created_and_updated_with_many_entity_links(self):
        todo = self.store.create_todo({"title": "Beleg prüfen"})
        termin = self.store.create_termin(
            {
                "title": "Rückfrage klären",
                "starts_at": "2026-07-01T10:00:00+02:00",
            }
        )

        created = self.store.create_vorgang(
            {
                "title": "Sammelvorgang",
                "description": "Mehrere Entitäten in einem Vorgang.",
                "vorgangstyp": "Klärung",
                "completed": True,
                "transaction_ids": ["tx_newer", "tx_older"],
                "todo_ids": [todo["todo_id"]],
                "beleg_ids": ["beleg_1"],
                "termin_ids": [termin["termin_id"]],
            }
        )

        self.assertTrue(created["vorgangs_id"].startswith("vorgang_"))
        self.assertEqual("abgeschlossen", created["status"])
        self.assertEqual(2, len(created["transaktionen"]))
        self.assertEqual([todo["todo_id"]], [item["todo_id"] for item in created["todos"]])
        self.assertEqual(
            [termin["termin_id"]],
            [item["termin_id"] for item in created["termine"]],
        )
        self.assertIn(
            created["vorgangs_id"],
            self.store.transaction_detail("tx_newer")["vorgangs_ids"],
        )

        updated = self.store.update_vorgang(
            created["vorgangs_id"],
            {
                "title": "Sammelvorgang aktualisiert",
                "completed": False,
                "transaction_ids": ["tx_newer"],
                "todo_ids": [],
                "beleg_ids": ["beleg_1"],
                "termin_ids": [termin["termin_id"]],
            },
        )

        self.assertEqual("Sammelvorgang aktualisiert", updated["titel"])
        self.assertEqual("in_bearbeitung", updated["status"])
        self.assertEqual(
            ["tx_newer"],
            [item["transaktions_id"] for item in updated["transaktionen"]],
        )
        self.assertEqual([], updated["todos"])

    def test_completed_vorgang_creation_rejects_incomplete_transactions(self):
        self.store.update_transaction_classification(
            "tx_older",
            {"unterkategorie": ""},
        )

        with self.assertRaisesRegex(ValueError, "Unterkategorie"):
            self.store.create_vorgang(
                {
                    "title": "Nicht abschließbar",
                    "completed": True,
                    "transaction_ids": ["tx_older"],
                }
            )

    def test_termine_can_be_created_linked_updated_and_deleted(self):
        termin = self.store.create_termin(
            {
                "title": "Vorstandssitzung",
                "description": "Quartalsplanung.",
                "starts_at": "2026-07-05T19:00:00+02:00",
                "ends_at": "2026-07-05T21:00:00+02:00",
                "location": "Vereinsheim",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )

        self.assertTrue(termin["termin_id"].startswith("termin_"))
        self.assertEqual("geplant", termin["status"])
        self.assertEqual(["vorgang_tx_newer"], termin["vorgangs_ids"])
        self.assertEqual(
            termin["termin_id"],
            self.store.vorgang_detail("vorgang_tx_newer")["termine"][0][
                "termin_id"
            ],
        )

        updated = self.store.update_termin(
            termin["termin_id"],
            {"status": "abgeschlossen", "vorgangs_ids": []},
        )
        self.assertEqual("abgeschlossen", updated["status"])
        self.assertEqual([], updated["vorgangs_ids"])
        self.assertEqual([], self.store.list_termine(hide_completed=True))

        deleted = self.store.delete_termin(termin["termin_id"])
        self.assertTrue(deleted["deleted"])

    def test_invalid_sort_is_rejected(self):
        with self.assertRaises(ValueError):
            self.store.list_transactions(sort="DROP TABLE transactions")


class DashboardHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        database_path = (
            Path(self.temporary_directory.name) / "transactions.sqlite3"
        )
        create_dashboard_database(database_path)
        self.player_payment_updates = []

        def update_player_payment(premium_name, payload):
            self.player_payment_updates.append((premium_name, payload))
            return {
                "season": "2025/2026",
                "generated_at": "2026-06-14T10:00:00+00:00",
                "counts": {
                    "eindeutig_gefunden": 0,
                    "manuell_pruefen": 1,
                    "nicht_gefunden": 0,
                },
                "players": [
                    {
                        "premium_name": premium_name,
                        "premium_total": 19.5,
                        "teams": [],
                        "member_name": "",
                        "match_quality": "kein_treffer",
                        "match_score": 0,
                        "status": "manuell_pruefen",
                        "candidate_count": 0,
                        "payment_source": "manual",
                        "masked_iban": "DE89 **** **** **** **30 00",
                        "bic": "COBADEFFXXX",
                        "iban_valid": True,
                        "bic_valid": True,
                        "iban_bic_assignment": "nicht_geprueft",
                        "manual_confirmation_required": True,
                        "approved_for_sepa": False,
                    }
                ],
                "teams": [],
                "team_groups": [],
                "manual_confirmation_required": True,
            }

        self.server = create_server(
            database_path,
            port=0,
            refresh_action=lambda: {
                "new_transactions": 2,
                "total_transactions": 4,
            },
            player_premium_action=lambda season, team_ids, point_values: {
                "season": season,
                "date_from": "2025-07-01",
                "date_to": "2026-06-30",
                "generated_at": "2026-06-12T10:00:00+00:00",
                "teams": [
                    {
                        "team_id": team_ids[0],
                        "label": "BSV - Herren 1",
                        "dfbnet_name": "BSV Viktoria Bielstein 1920 e.V.",
                        "matches": [],
                        "players": [],
                        "point_value": float(point_values[team_ids[0]]),
                        "premium_total": 0,
                    }
                ],
            },
            player_payment_action=lambda premium_result, deckel_path=None: {
                "season": (
                    premium_result["season"]
                    if premium_result
                    else "2025/2026"
                ),
                "generated_at": "2026-06-13T10:00:00+00:00",
                "counts": {
                    "eindeutig_gefunden": 1,
                    "manuell_pruefen": 0,
                    "nicht_gefunden": 0,
                },
                "players": [
                    {
                        "premium_name": "Max Mustermann",
                        "premium_total": 19.5,
                        "teams": [],
                        "member_name": "Max Mustermann",
                        "match_quality": "exakt",
                        "match_score": 1,
                        "status": "eindeutig_gefunden",
                        "candidate_count": 1,
                        "masked_iban": "DE89 **** **** **** **30 00",
                        "bic": "COBADEFFXXX",
                        "iban_valid": True,
                        "bic_valid": True,
                        "iban_bic_assignment": "nicht_geprueft",
                        "manual_confirmation_required": True,
                        "approved_for_sepa": False,
                    }
                ],
                "manual_confirmation_required": True,
            },
            player_payment_update_action=update_player_payment,
            mail_backend=FakeDashboardMailBackend(),
            mail_spam_scorer=FakeDashboardSpamScorer(),
        )
        self.server.mail_vorgang_analyzer = FakeMailVorgangAnalyzer()
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True,
        )
        self.thread.start()
        self.base_url = (
            f"http://127.0.0.1:{self.server.server_address[1]}"
        )

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        self.temporary_directory.cleanup()

    def test_balance_correction_api_validates_persists_and_is_idempotent(self):
        payload = {
            "account_id": "acct_test",
            "balance_minor": 12345,
            "balance_as_of": "2026-06-10",
            "reason": "Kontoauszug manuell geprueft",
        }
        request = Request(
            self.base_url + "/api/balance-corrections",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 201)
            created = json.load(response)["correction"]
        self.assertEqual(created["balance_minor"], 12345)
        self.assertEqual(created["account_number"], "DE001")
        self.assertTrue(created["is_manual"])
        self.assertIn("manueller Pruefung", created["usage_notice"])

        with urlopen(request, timeout=5) as response:
            duplicate = json.load(response)["correction"]
        self.assertEqual(duplicate["correction_id"], created["correction_id"])
        with urlopen(self.base_url + "/api/balance-corrections", timeout=5) as response:
            listed = json.load(response)
        self.assertEqual(listed["count"], 1)

        invalid = Request(
            self.base_url + "/api/balance-corrections",
            data=json.dumps({**payload, "balance_minor": "12345"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as caught:
            urlopen(invalid, timeout=5)
        self.assertEqual(caught.exception.code, 400)

    def test_balance_summary_exposes_known_accounts_for_correction_form(self):
        with urlopen(self.base_url + "/api/transactions", timeout=5) as response:
            balances = json.load(response)["balances"]

        account = next(
            item for item in balances["konten"] if item["account_id"] == "acct_test"
        )
        self.assertEqual(account["provider"], "testbank")
        self.assertEqual(account["kontoname"], "Hauptkonto")

    def test_dashboard_contains_balance_correction_ui_flow(self):
        with urlopen(self.base_url + "/", timeout=5) as response:
            html = response.read().decode("utf-8")
        with urlopen(self.base_url + "/static/app.js", timeout=5) as response:
            javascript = response.read().decode("utf-8")

        self.assertIn('id="balance-correction-form"', html)
        self.assertIn('name="manual_confirmation"', html)
        self.assertIn("keine Originaltransaktionen", html)
        self.assertIn('fetch("/api/balance-corrections"', javascript)
        self.assertIn("balance_minor: Number(rawAmount)", javascript)
        self.assertNotIn("delete-balance-correction", html)

    def test_vorgang_create_form_offers_create_and_complete_action(self):
        javascript = (
            Path(__file__).parents[1] / "banking_dashboard/static/app.js"
        ).read_text(encoding="utf-8")

        self.assertIn('"Vorgang erstellen und abschließen"', javascript)
        self.assertIn('completeSubmit.dataset.completed = "true"', javascript)
        self.assertIn(
            'event.submitter?.dataset.completed === "true"',
            javascript,
        )
        self.assertIn(
            "readVorgangForm(form, completeRequested)",
            javascript,
        )
        self.assertIn('actions.append(submit, completeSubmit, status)', javascript)

    def test_balance_corrections_are_collapsed_before_transaction_table(self):
        with urlopen(self.base_url + "/", timeout=5) as response:
            html = response.read().decode("utf-8")

        corrections_start = html.index('<details class="balance-corrections">')
        corrections_end = html.index("</details>", corrections_start)
        transaction_table = html.index('id="transaction-table"')

        self.assertNotIn(" open", html[corrections_start:corrections_end])
        self.assertLess(corrections_end, transaction_table)
        self.assertIn('id="total-balance-note"', html[:corrections_start])
        self.assertIn('class="balance-note"', html[:corrections_start])

    def test_assignment_dialog_submit_flow_handles_validation_success_and_error(self):
        javascript_path = Path(__file__).parents[1] / "banking_dashboard/static/app.js"
        javascript = javascript_path.read_text(encoding="utf-8")

        def function_source(name):
            start = javascript.index(f"function {name}")
            if javascript[max(0, start - 6):start] == "async ":
                start -= 6
            opening_brace = javascript.index("{", javascript.index(")", start))
            depth = 0
            for index in range(opening_brace, len(javascript)):
                if javascript[index] == "{":
                    depth += 1
                elif javascript[index] == "}":
                    depth -= 1
                    if depth == 0:
                        return javascript[start:index + 1]
            self.fail(f"JavaScript-Funktion {name} ist nicht vollständig.")

        node_test = "\n".join([
            function_source("setAssignmentStatus"),
            function_source("submitVorgangAssignment"),
            r"""
const assert = require("node:assert/strict");
const controls = () => ({form: {dataset: {}}, submit: {disabled: false}, status: {}});

(async () => {
  const missing = controls();
  let requests = 0;
  const missingResult = await submitVorgangAssignment({
    ...missing, selectedId: "", request: async () => { requests += 1; }, onSaved: async () => {},
  });
  assert.equal(missingResult, false);
  assert.equal(requests, 0);
  assert.equal(missing.status.textContent, "Bitte zuerst einen Vorgang auswählen.");
  assert.equal(missing.status.className, "save-state is-error");

  const success = controls();
  let releaseRequest;
  const pendingRequest = new Promise((resolve) => { releaseRequest = resolve; });
  let saved = 0;
  const first = submitVorgangAssignment({
    ...success, selectedId: "vorgang-1",
    request: async () => { requests += 1; await pendingRequest; },
    onSaved: async () => { saved += 1; },
  });
  const duplicate = await submitVorgangAssignment({
    ...success, selectedId: "vorgang-1",
    request: async () => { requests += 1; }, onSaved: async () => { saved += 1; },
  });
  assert.equal(duplicate, false);
  assert.equal(requests, 1);
  assert.equal(success.submit.disabled, true);
  assert.equal(success.status.textContent, "Zuordnung wird gespeichert");
  releaseRequest();
  assert.equal(await first, true);
  assert.equal(saved, 1);
  assert.equal(success.status.textContent, "Zuordnung gespeichert");
  assert.equal(success.status.className, "save-state is-saved");

  const failed = controls();
  const failedResult = await submitVorgangAssignment({
    ...failed, selectedId: "vorgang-2",
    request: async () => { throw new Error("Vorgang ist abgeschlossen"); },
    onSaved: async () => { throw new Error("darf nicht laufen"); },
  });
  assert.equal(failedResult, false);
  assert.equal(failed.form.dataset.assignmentSaving, undefined);
  assert.equal(failed.submit.disabled, false);
  assert.equal(failed.status.className, "save-state is-error");
  assert.equal(failed.status.textContent, "Zuordnung fehlgeschlagen: Vorgang ist abgeschlossen");
})().catch((error) => { console.error(error); process.exit(1); });
""",
        ])
        result = subprocess.run(
            ["node", "-e", node_test],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertGreaterEqual(javascript.count("submitVorgangAssignment({"), 4)
        for form_name in ("renderTodoEntityForm", "renderTerminEntityForm"):
            form_source = function_source(form_name)
            self.assertIn("await submitVorgangAssignment({", form_source)
            self.assertIn('selectedId: selectedIds[0] || ""', form_source)
            self.assertNotIn("actions.submit.disabled = true", form_source)
        self.assertIn("renderBelegEntityPreview(beleg.beleg_id, \"Zuordnung gespeichert\")", javascript)
        self.assertIn('elements.detailDialogStatus.textContent = "Zuordnung gespeichert"', javascript)

    def test_todo_and_termin_lists_distinguish_empty_filtered_and_error_states(self):
        root = Path(__file__).parents[1]
        html = (root / "banking_dashboard/static/index.html").read_text(
            encoding="utf-8"
        )
        javascript = (root / "banking_dashboard/static/app.js").read_text(
            encoding="utf-8"
        )

        self.assertRegex(
            html,
            r'id="todo-empty" role="status" aria-live="polite"',
        )
        self.assertRegex(
            html,
            r'id="termin-empty" role="status" aria-live="polite"',
        )

        def function_source(name):
            start = javascript.index(f"function {name}")
            if javascript[max(0, start - 6):start] == "async ":
                start -= 6
            opening_brace = javascript.index("{", javascript.index(")", start))
            depth = 0
            for index in range(opening_brace, len(javascript)):
                if javascript[index] == "{":
                    depth += 1
                elif javascript[index] == "}":
                    depth -= 1
                    if depth == 0:
                        return javascript[start:index + 1]
            self.fail(f"JavaScript-Funktion {name} ist nicht vollständig.")

        node_test = "\n".join([
            function_source("loadTodos"),
            function_source("renderTodoList"),
            function_source("loadTermine"),
            function_source("renderTerminList"),
            r"""
const assert = require("node:assert/strict");

function emptyElement() {
  const classes = new Set();
  return {
    hidden: false,
    textContent: "",
    classList: {
      toggle(name, enabled) {
        if (enabled) classes.add(name); else classes.delete(name);
      },
      contains(name) { return classes.has(name); },
    },
  };
}

function listElement() {
  return {
    children: [],
    replaceChildren(...children) { this.children = children; },
  };
}

const elements = {
  todoEmpty: emptyElement(),
  todoList: listElement(),
  todoLoading: emptyElement(),
  todoCount: emptyElement(),
  todoCountLabel: emptyElement(),
  terminEmpty: emptyElement(),
  terminList: listElement(),
  terminLoading: emptyElement(),
  terminCount: emptyElement(),
  terminCountLabel: emptyElement(),
};
const state = {
  todos: [], todoSearch: "", todoHideCompleted: false,
  todoVorgaenge: [{}], editingTodoId: null, todosLoaded: false,
  termine: [], terminSearch: "", terminHideCompleted: false,
  terminUnassignedUpcoming: false,
  terminVorgaenge: [{}], editingTerminId: null, termineLoaded: false,
};
const integerFormatter = new Intl.NumberFormat("de-DE");

async function readResponse(response) { return response.payload; }
function showError(error) { throw new Error(error); }

const requestedUrls = [];
async function fetch(url) {
  requestedUrls.push(url);
  if (url.startsWith("/api/todos?")) {
    const parameters = new URL(url, "https://dashboard.test").searchParams;
    assert.equal(parameters.get("search"), "nicht vorhanden");
    return {payload: {todos: [], count: 0}};
  }
  if (url.startsWith("/api/termine?")) {
    const parameters = new URL(url, "https://dashboard.test").searchParams;
    assert.equal(parameters.get("unassigned_upcoming"), "true");
    return {payload: {termine: [], count: 0}};
  }
  throw new Error(`Unerwarteter Request: ${url}`);
}

function assertListState(render, empty, expectedText, isError = false) {
  render();
  assert.equal(empty.hidden, false);
  assert.equal(empty.textContent, expectedText);
  assert.equal(empty.classList.contains("is-error"), isError);
}

assertListState(
  renderTodoList,
  elements.todoEmpty,
  "Noch keine To-Dos vorhanden.",
);

(async () => {
  state.todos = [{todo_id: "todo-1", title: "Beitrag prüfen"}];
  elements.todoList.children = [{dataset: {todoId: "todo-1"}}];
  state.todoSearch = "nicht vorhanden";
  await loadTodos();
  assert.equal(requestedUrls[0].startsWith("/api/todos?"), true);
  assert.equal(state.todos.length, 0);
  assert.equal(elements.todoList.children.length, 0);
  assertListState(
    renderTodoList,
    elements.todoEmpty,
    "Keine To-Dos entsprechen der aktuellen Suche oder Filterung.",
  );
  state.todoSearch = "";
  assertListState(
    () => renderTodoList("Netzwerkfehler"),
    elements.todoEmpty,
    "To-Dos konnten nicht geladen werden. Bitte versuchen Sie es erneut.",
    true,
  );

  assertListState(
    renderTerminList,
    elements.terminEmpty,
    "Noch keine Termine vorhanden.",
  );
  state.termine = [{termin_id: "termin-1", title: "Training"}];
  elements.terminList.children = [{dataset: {terminId: "termin-1"}}];
  state.terminUnassignedUpcoming = true;
  await loadTermine();
  assert.equal(requestedUrls[1].startsWith("/api/termine?"), true);
  assert.equal(state.termine.length, 0);
  assert.equal(elements.terminList.children.length, 0);
  assertListState(
    renderTerminList,
    elements.terminEmpty,
    "Keine Termine entsprechen der aktuellen Suche oder Filterung.",
  );
  state.terminUnassignedUpcoming = false;
  assertListState(
    () => renderTerminList("Netzwerkfehler"),
    elements.terminEmpty,
    "Termine konnten nicht geladen werden. Bitte versuchen Sie es erneut.",
    true,
  );
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
""",
        ])
        result = subprocess.run(
            ["node", "-e", node_test],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_todo_load_error_invalidates_count_and_previous_filter_results(self):
        javascript = (
            Path(__file__).parents[1] / "banking_dashboard/static/app.js"
        ).read_text(encoding="utf-8")

        def function_source(name):
            start = javascript.index(f"function {name}")
            if javascript[max(0, start - 6):start] == "async ":
                start -= 6
            opening_brace = javascript.index("{", javascript.index(")", start))
            depth = 0
            for index in range(opening_brace, len(javascript)):
                if javascript[index] == "{":
                    depth += 1
                elif javascript[index] == "}":
                    depth -= 1
                    if depth == 0:
                        return javascript[start:index + 1]
            self.fail(f"JavaScript-Funktion {name} ist nicht vollständig.")

        node_test = "\n".join([
            function_source("loadTodos"),
            function_source("renderTodoList"),
            r"""
const assert = require("node:assert/strict");
function element() {
  const classes = new Set();
  return {
    hidden: false, textContent: "", children: [],
    replaceChildren(...children) { this.children = children; },
    classList: {
      toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); },
      contains(name) { return classes.has(name); },
    },
  };
}
const elements = {
  todoLoading: element(), todoEmpty: element(), todoList: element(),
  todoCount: element(), todoCountLabel: element(),
};
const state = {
  todos: [{todo_id: "alt", title: "Altes Filterresultat", completed: false}],
  todoSearch: "offen", todoHideCompleted: false,
  todoVorgaenge: [{}], editingTodoId: null, todosLoaded: true,
};
const integerFormatter = new Intl.NumberFormat("de-DE");
let fail = true;
async function fetch() {
  if (fail) throw new Error("Netzwerkfehler");
  return {payload: {todos: [], count: 0}};
}
async function readResponse(response) { return response.payload; }
const shownErrors = [];
function showError(message) { shownErrors.push(message); }
function mailElement() { throw new Error("Bei leeren Resultaten nicht erwartet"); }

(async () => {
  elements.todoCount.textContent = "1";
  elements.todoCountLabel.textContent = "To-Do";
  elements.todoList.children = [{dataset: {todoId: "alt"}}];
  await loadTodos();
  assert.deepEqual(state.todos, []);
  assert.deepEqual(elements.todoList.children, []);
  assert.equal(elements.todoCount.textContent, "–");
  assert.equal(elements.todoCountLabel.textContent, "Nicht verfügbar");
  assert.equal(elements.todoEmpty.classList.contains("is-error"), true);
  assert.match(elements.todoEmpty.textContent, /konnten nicht geladen werden/);

  fail = false;
  await loadTodos();
  assert.equal(elements.todoCount.textContent, "0");
  assert.equal(elements.todoCountLabel.textContent, "To-Dos");
  assert.equal(elements.todoEmpty.classList.contains("is-error"), false);
  assert.match(elements.todoEmpty.textContent, /Keine To-Dos entsprechen/);
})().catch((error) => { console.error(error); process.exitCode = 1; });
""",
        ])
        result = subprocess.run(
            ["node", "-e", node_test],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        for list_name in ("transaction", "vorgang", "todo", "termin"):
            self.assertIn(
                f'elements.{list_name}Count.textContent = "–";', javascript
            )
        self.assertIn('elements.budgetCount.textContent = loadError', javascript)

    def test_donation_certificate_api_creates_cent_exact_linked_html(self):
        database_path = self.server.data_store.database_path
        with closing(connect_database(database_path)) as connection:
            connection.execute(
                """
                INSERT INTO donation_recipients (
                    recipient_id, name, address_addition, street,
                    house_number, postal_code, city, country,
                    created_at, updated_at
                ) VALUES (
                    'recipient_1', 'Erika Beispiel', '', 'Testweg',
                    '7', '51674', 'Wiehl', 'Deutschland',
                    '2026-07-12T10:00:00Z', '2026-07-12T10:00:00Z'
                )
                """
            )
            connection.commit()

        endpoint = self.base_url + "/api/vorgaenge/vorgang_tx_newer/spendenbescheinigung"
        request = Request(
            endpoint,
            data=json.dumps({"recipient_id": "recipient_1"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(201, response.status)
            result = json.load(response)
        with closing(sqlite3.connect(database_path)) as connection:
            expected_minor = connection.execute(
                """
                SELECT t.amount_minor FROM transactions AS t
                JOIN transaktion_vorgaenge AS tv
                  ON tv.transaktions_id = t.transaction_id
                WHERE tv.vorgangs_id = 'vorgang_tx_newer'
                """
            ).fetchone()[0]
        self.assertEqual(expected_minor, result["amount_minor"])
        beleg = result["beleg"]
        self.assertEqual("automatic", beleg["quelle"])
        self.assertEqual("spendenbescheinigungen", beleg["kategorie"])
        self.assertEqual(["vorgang_tx_newer"], beleg["vorgangs_ids"])
        content = Path(beleg["dateipfad"]).read_text(encoding="utf-8")
        self.assertIn("Erika Beispiel", content)
        self.assertIn("vorgang_tx_newer", content)
        self.assertIn(f"{expected_minor / 100:.2f} EUR", content)

        with closing(connect_database(database_path)) as connection:
            link = connection.execute(
                "SELECT vorgangs_id FROM vorgang_belege WHERE beleg_id = ?",
                (beleg["beleg_id"],),
            ).fetchall()
        self.assertEqual([("vorgang_tx_newer",)], [tuple(row) for row in link])

    def test_donation_certificate_api_rejects_unknown_ids_without_changes(self):
        database_path = self.server.data_store.database_path
        before_files = set(self.server.data_store.belege_directory.rglob("*"))
        for vorgangs_id, recipient_id in (
            ("vorgang_tx_newer", "recipient_missing"),
            ("vorgang_missing", "recipient_missing"),
        ):
            request = Request(
                self.base_url + f"/api/vorgaenge/{vorgangs_id}/spendenbescheinigung",
                data=json.dumps({"recipient_id": recipient_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)
            self.assertIn(raised.exception.code, {400, 404})
        with closing(connect_database(database_path)) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM belege WHERE quelle = 'automatic'"
            ).fetchone()[0]
        self.assertEqual(0, count)
        self.assertEqual(before_files, set(self.server.data_store.belege_directory.rglob("*")))

    def test_donation_certificate_api_rejects_invalid_recipient_id_without_changes(self):
        database_path = self.server.data_store.database_path
        endpoint = self.base_url + "/api/vorgaenge/vorgang_tx_newer/spendenbescheinigung"
        before_files = set(self.server.data_store.belege_directory.rglob("*"))
        with closing(connect_database(database_path)) as connection:
            before_belege = connection.execute(
                "SELECT COUNT(*) FROM belege"
            ).fetchone()[0]
            before_links = connection.execute(
                "SELECT COUNT(*) FROM vorgang_belege"
            ).fetchone()[0]

        for recipient_id in (None, 123, "", "   "):
            request = Request(
                endpoint,
                data=json.dumps({"recipient_id": recipient_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)
            self.assertEqual(400, raised.exception.code)

        with closing(connect_database(database_path)) as connection:
            self.assertEqual(
                before_belege,
                connection.execute(
                    "SELECT COUNT(*) FROM belege"
                ).fetchone()[0],
            )
            self.assertEqual(
                before_links,
                connection.execute(
                    "SELECT COUNT(*) FROM vorgang_belege"
                ).fetchone()[0],
            )
        self.assertEqual(
            before_files,
            set(self.server.data_store.belege_directory.rglob("*")),
        )

    def test_mail_document_assignment_api_validates_vorgang_context(self):
        database_path = self.server.data_store.database_path
        with closing(connect_database(database_path)) as connection:
            connection.execute(
                """
                UPDATE transaktion_vorgaenge
                SET bezugs_id = 'tvb_newer'
                WHERE transaktions_id = 'tx_newer'
                  AND vorgangs_id = 'vorgang_tx_newer'
                """
            )
            connection.execute(
                """
                UPDATE transaktion_vorgaenge
                SET bezugs_id = 'tvb_older'
                WHERE transaktions_id = 'tx_older'
                  AND vorgangs_id = 'vorgang_tx_older'
                """
            )
            connection.commit()

        endpoint = (
            self.base_url
            + "/api/vorgaenge/vorgang_tx_newer/mail-dokumentzuordnungen"
        )
        with urlopen(endpoint, timeout=5) as response:
            initial = json.load(response)
        self.assertEqual("vorgang_tx_newer", initial["vorgang"]["vorgangs_id"])
        self.assertEqual(
            ["tx_newer"],
            [item["transaktions_id"] for item in initial["transaktionen"]],
        )
        self.assertEqual(["beleg_1"], [item["beleg_id"] for item in initial["dokumente"]])
        self.assertIsNone(initial["zuordnungen"][0]["transaktions_id"])

        update = Request(
            endpoint,
            data=json.dumps(
                {
                    "vorgangs_id": "vorgang_tx_newer",
                    "zuordnungen": [
                        {"beleg_id": "beleg_1", "transaktions_id": "tx_newer"}
                    ],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urlopen(update, timeout=5) as response:
            assigned = json.load(response)
        self.assertEqual("tx_newer", assigned["zuordnungen"][0]["transaktions_id"])

        # Derselbe Zustand ist idempotent.
        with urlopen(update, timeout=5) as response:
            duplicate = json.load(response)
        self.assertEqual(assigned["zuordnungen"], duplicate["zuordnungen"])

        invalid_payloads = (
            ({"zuordnungen": [{"beleg_id": "missing", "transaktions_id": None}]}, 404),
            ({"zuordnungen": [{"beleg_id": "beleg_1", "transaktions_id": "missing"}]}, 404),
            ({"zuordnungen": [{"beleg_id": "beleg_1", "transaktions_id": "tx_older"}]}, 400),
            ({"vorgangs_id": "vorgang_tx_older", "zuordnungen": []}, 400),
            ({"zuordnungen": [], "direkte_beziehung": True}, 400),
        )
        for payload, expected_status in invalid_payloads:
            with self.subTest(payload=payload):
                request = Request(
                    endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="PUT",
                )
                with self.assertRaises(HTTPError) as error:
                    urlopen(request, timeout=5)
                self.assertEqual(expected_status, error.exception.code)

        with urlopen(endpoint, timeout=5) as response:
            unchanged = json.load(response)
        self.assertEqual("tx_newer", unchanged["zuordnungen"][0]["transaktions_id"])

        with closing(connect_database(database_path)) as connection:
            self.assertNotIn(
                "transaktions_id",
                {
                    str(row["name"])
                    for row in connection.execute("PRAGMA table_info(vorgang_belege)")
                },
            )

    def test_created_vorgang_keeps_resolvable_document_assignment_on_update(self):
        created = self.server.data_store.create_vorgang(
            {
                "title": "Mail-Dokumentzuordnung",
                "transaction_ids": ["tx_newer"],
                "beleg_ids": ["beleg_1"],
            }
        )
        vorgangs_id = created["vorgangs_id"]
        endpoint = (
            self.base_url
            + f"/api/vorgaenge/{vorgangs_id}/mail-dokumentzuordnungen"
        )
        update = Request(
            endpoint,
            data=json.dumps(
                {
                    "zuordnungen": [
                        {"beleg_id": "beleg_1", "transaktions_id": "tx_newer"}
                    ]
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urlopen(update, timeout=5) as response:
            assigned = json.load(response)
        self.assertEqual("tx_newer", assigned["zuordnungen"][0]["transaktions_id"])

        self.server.data_store.update_vorgang(
            vorgangs_id,
            {"title": "Mail-Dokumentzuordnung aktualisiert"},
        )

        with urlopen(endpoint, timeout=5) as response:
            reloaded = json.load(response)
        self.assertEqual("tx_newer", reloaded["zuordnungen"][0]["transaktions_id"])
        with closing(
            connect_database(self.server.data_store.database_path)
        ) as connection:
            reference = connection.execute(
                """
                SELECT bezugs_id
                FROM transaktion_vorgaenge
                WHERE vorgangs_id = ? AND transaktions_id = 'tx_newer'
                """,
                (vorgangs_id,),
            ).fetchone()["bezugs_id"]
        self.assertTrue(str(reference).startswith("tvb_"))

    def test_dashboard_and_api_are_served(self):
        with urlopen(self.base_url + "/", timeout=5) as response:
            html = response.read().decode("utf-8")
            self.assertIn("Banking Dashboard", html)
            self.assertIn("Content-Security-Policy", response.headers)

        with urlopen(
            self.base_url
            + "/api/transactions?sort=betrag&direction=asc&search=12%2C34",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["count"], 1)
            self.assertFalse(payload["hide_completed_vorgaenge"])
            self.assertEqual(
                payload["transactions"][0]["transaktions_id"],
                "tx_older",
            )
            self.assertIn("vorgaenge_count", payload["transactions"][0])
            self.assertIn(
                "completed_vorgaenge_count",
                payload["transactions"][0],
            )
            self.assertIn("has_vorgaenge", payload["transactions"][0])
            self.assertIn(
                "has_completed_vorgaenge",
                payload["transactions"][0],
            )

        with closing(connect_database(self.server.data_store.database_path)) as connection:
            connection.execute(
                """
                UPDATE transactions
                SET sphere = ''
                WHERE transaction_id = 'tx_older'
                """
            )
            connection.commit()
        with urlopen(
            self.base_url + "/api/transactions?unclassified_only=true",
            timeout=5,
        ) as response:
            payload = json.load(response)
        self.assertTrue(payload["unclassified_only"])
        self.assertEqual(
            [item["transaktions_id"] for item in payload["transactions"]],
            ["tx_older"],
        )

        with urlopen(
            self.base_url + "/api/transactions/tx_newer",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertNotIn("beleg_ids", payload["transaction"])
            self.assertEqual(
                payload["transaction"]["splits"][0]["split_id"],
                "split_tx_newer_1",
            )
        with urlopen(
            self.base_url + "/api/transactions/tx_newer/splits",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["transaction_id"], "tx_newer")
            self.assertEqual(payload["amount_minor"], 2500)
            self.assertEqual(payload["betrag_cent"], 2500)
            self.assertEqual(payload["betrag"], "25.00")
            self.assertEqual(
                payload["splits"][0]["amount_minor"],
                1500,
            )
            self.assertEqual(payload["splits"][0]["sort_order"], 0)
            self.assertEqual(
                payload["splits"][0]["transaction_id"],
                "tx_newer",
            )
            self.assertEqual(
                payload["zulaessige_vorgaenge"][0]["vorgangs_id"],
                "vorgang_tx_newer",
            )
            self.assertEqual(
                payload["zulaessige_vorgaenge"][0]["titel"],
                "",
            )
            self.assertEqual(
                payload["zulaessige_vorgaenge"][0]["status"],
                "in_bearbeitung",
            )
            self.assertEqual(
                payload["zulaessige_vorgaenge"][0]["belege"][0]["dateiname"],
                "beleg_1.pdf",
            )

        request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=json.dumps(
                {
                    "splits": [
                        {
                            "amount_minor": 1000,
                            "description": "API Teil 1",
                            "transaction_type": "Einnahme",
                            "top_category": "Spielbetrieb",
                            "sub_category": "Eintritt",
                            "sphere": "Zweckbetrieb",
                        },
                        {
                            "amount_minor": 1500,
                            "description": "API Teil 2",
                            "transaction_type": "Einnahme",
                            "top_category": "Spielbetrieb",
                            "sub_category": "Eintritt",
                            "sphere": "Zweckbetrieb",
                        },
                    ]
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)
            self.assertEqual(
                [split["amount_minor"] for split in payload[
                    "transaction"
                ]["splits"]],
                [1000, 1500],
            )
            self.assertEqual(
                [split["sort_order"] for split in payload[
                    "transaction"
                ]["splits"]],
                [1, 2],
            )

        invalid_request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=json.dumps(
                {"splits": [{"betrag_cent": 2499}]}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as invalid_error:
            urlopen(invalid_request, timeout=5)
        self.assertEqual(invalid_error.exception.code, 400)
        error_payload = json.loads(
            invalid_error.exception.read().decode("utf-8")
        )
        self.assertIn("Erwartet: 2500 Cent", error_payload["error"])
        self.assertIn("Split-Summe: 2499 Cent", error_payload["error"])
        self.assertIn("Differenz: -1 Cent", error_payload["error"])
        with urlopen(
            self.base_url + "/api/transactions/tx_newer",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [split["betrag_cent"] for split in payload[
                    "transaction"
                ]["splits"]],
                [1000, 1500],
            )

        duplicate_id_request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=json.dumps(
                {
                    "splits": [
                        {
                            "split_id": "split_api_duplicate",
                            "betrag_cent": 1000,
                        },
                        {
                            "split_id": "split_api_duplicate",
                            "betrag_cent": 1500,
                        },
                    ]
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as duplicate_id_error:
            urlopen(duplicate_id_request, timeout=5)
        self.assertEqual(duplicate_id_error.exception.code, 400)
        with urlopen(
            self.base_url + "/api/transactions/tx_newer/splits",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [split["betrag_cent"] for split in payload["splits"]],
                [1000, 1500],
            )

        mismatched_transaction_request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=json.dumps(
                {
                    "splits": [
                        {
                            "transaction_id": "tx_older",
                            "betrag_cent": 2500,
                        },
                    ]
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as mismatched_error:
            urlopen(mismatched_transaction_request, timeout=5)
        self.assertEqual(mismatched_error.exception.code, 400)
        with urlopen(
            self.base_url + "/api/transactions/tx_newer/splits",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [split["betrag_cent"] for split in payload["splits"]],
                [1000, 1500],
            )

        unknown_field_request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=json.dumps(
                {"splits": [{"betrag_cent": 2500, "unexpected": "x"}]}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as unknown_field_error:
            urlopen(unknown_field_request, timeout=5)
        self.assertEqual(unknown_field_error.exception.code, 400)
        with urlopen(
            self.base_url + "/api/transactions/tx_newer/splits",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [split["betrag_cent"] for split in payload["splits"]],
                [1000, 1500],
            )

        malformed_json_request = Request(
            self.base_url + "/api/transactions/tx_newer/splits",
            data=b'{"splits": [',
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as malformed_json_error:
            urlopen(malformed_json_request, timeout=5)
        self.assertEqual(malformed_json_error.exception.code, 400)
        self.assertEqual(
            json.loads(
                malformed_json_error.exception.read().decode("utf-8")
            ),
            {"error": "Ungültiger JSON-Inhalt."},
        )
        with urlopen(
            self.base_url + "/api/transactions/tx_newer/splits",
            timeout=5,
        ) as response:
            payload = json.load(response)
        self.assertEqual(
            [split["betrag_cent"] for split in payload["splits"]],
            [1000, 1500],
        )

        for invalid_amount in (2500.0, "2500", True):
            with self.subTest(invalid_amount=invalid_amount):
                invalid_type_request = Request(
                    self.base_url + "/api/transactions/tx_newer/splits",
                    data=json.dumps(
                        {"splits": [{"betrag_cent": invalid_amount}]}
                    ).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="PUT",
                )
                with self.assertRaises(HTTPError) as invalid_type_error:
                    urlopen(invalid_type_request, timeout=5)
                self.assertEqual(invalid_type_error.exception.code, 400)
                self.assertIn(
                    "ganzzahligen Betrag",
                    json.loads(
                        invalid_type_error.exception.read().decode("utf-8")
                    )["error"],
                )
                with urlopen(
                    self.base_url + "/api/transactions/tx_newer/splits",
                    timeout=5,
                ) as response:
                    payload = json.load(response)
                self.assertEqual(
                    [split["betrag_cent"] for split in payload["splits"]],
                    [1000, 1500],
                )

        for path in (
            "/api/transactions/tx_missing/splits",
            "/api/transactions//splits",
        ):
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as get_error:
                    urlopen(self.base_url + path, timeout=5)
                self.assertEqual(
                    get_error.exception.code,
                    404 if "tx_missing" in path else 400,
                )
                self.assertTrue(
                    json.loads(
                        get_error.exception.read().decode("utf-8")
                    )["error"]
                )

        missing_request = Request(
            self.base_url + "/api/transactions/tx_missing/splits",
            data=json.dumps({"splits": []}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with self.assertRaises(HTTPError) as missing_error:
            urlopen(missing_request, timeout=5)
        self.assertEqual(missing_error.exception.code, 404)

        with urlopen(
            self.base_url + "/api/vorgaenge",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["count"], 2)
            self.assertEqual(
                payload["vorgaenge"][0]["vorgangs_id"],
                "vorgang_tx_newer",
            )

        self.server.data_store.update_transaction_classification(
            "tx_newer",
            {"transaktionstyp": "Vergütung"},
        )
        with urlopen(
            self.base_url + "/api/vorgaenge",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [row["vorgangs_id"] for row in payload["vorgaenge"]],
                ["vorgang_tx_older", "vorgang_tx_newer"],
            )
            self.assertEqual(
                [row["status"] for row in payload["vorgaenge"]],
                ["in_bearbeitung", "abgeschlossen"],
            )

        with urlopen(
            self.base_url + "/api/vorgaenge?search=Verein",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [row["vorgangs_id"] for row in payload["vorgaenge"]],
                ["vorgang_tx_older", "vorgang_tx_newer"],
            )

        with urlopen(
            self.base_url + "/api/transactions?hide_completed_vorgaenge=true",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertTrue(payload["hide_completed_vorgaenge"])
            self.assertEqual(payload["count"], 1)
            self.assertEqual(
                payload["transactions"][0]["transaktions_id"],
                "tx_older",
            )

        with urlopen(
            self.base_url + "/api/vorgaenge?hide_completed=true",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertTrue(payload["hide_completed"])
            self.assertEqual(payload["count"], 1)
            self.assertTrue(
                all(
                    row["status"] != "abgeschlossen"
                    for row in payload["vorgaenge"]
                )
            )

        with urlopen(
            self.base_url
            + "/api/vorgaenge?search=Neuer%20Verein&hide_completed=false",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["search"], "Neuer Verein")
            self.assertFalse(payload["hide_completed"])
            self.assertEqual(payload["count"], 1)
            self.assertEqual(
                payload["vorgaenge"][0]["vorgangs_id"],
                "vorgang_tx_newer",
            )
            self.assertEqual(
                payload["vorgaenge"][0]["status"],
                "abgeschlossen",
            )

        with urlopen(
            self.base_url
            + "/api/vorgaenge?search=Neuer%20Verein&hide_completed=true",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertTrue(payload["hide_completed"])
            self.assertEqual(payload["count"], 0)
            self.assertEqual(payload["vorgaenge"], [])

        with urlopen(
            self.base_url + "/api/vorgaenge?search=Kein%20Treffer",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["count"], 0)
            self.assertEqual(payload["vorgaenge"], [])

        with urlopen(
            self.base_url + "/api/vorgaenge/vorgang_tx_newer",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                payload["vorgang"]["transaktionen"][0]["transaktions_id"],
                "tx_newer",
            )

        with urlopen(
            self.base_url + "/api/classification-options",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertIn("Ausgabe", payload["transaction_types"])
            self.assertEqual(len(payload["spheres"]), 4)

        with urlopen(
            self.base_url
            + "/api/balance-history?date_from=2026-05-01&date_to=2026-06-10",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(payload["series"][0]["id"], "gesamt")

    def test_transaction_vorgang_link_api_is_idempotent(self):
        link_request = Request(
            self.base_url + "/api/transactions/tx_newer/vorgaenge",
            data=json.dumps({"vorgangs_id": "vorgang_tx_older"}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(link_request, timeout=5) as response:
            linked = json.load(response)
        duplicate_request = Request(
            self.base_url + "/api/transactions/tx_newer/vorgaenge",
            data=json.dumps({"vorgangs_id": "vorgang_tx_older"}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(duplicate_request, timeout=5) as response:
            duplicate = json.load(response)

        self.assertEqual(
            ["vorgang_tx_newer", "vorgang_tx_older"],
            sorted(linked["transaction"]["vorgangs_ids"]),
        )
        self.assertEqual(
            ["vorgang_tx_newer", "vorgang_tx_older"],
            sorted(duplicate["transaction"]["vorgangs_ids"]),
        )

        unknown_request = Request(
            self.base_url + "/api/transactions/tx_newer/vorgaenge",
            data=json.dumps({"vorgangs_id": "vorgang_unbekannt"}).encode(
                "utf-8"
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as error:
            urlopen(unknown_request, timeout=5)
        self.assertEqual(404, error.exception.code)

        with closing(connect_database(
            self.server.data_store.database_path
        )) as connection:
            link_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM transaktion_vorgaenge
                WHERE transaktions_id = 'tx_newer'
                  AND vorgangs_id = 'vorgang_tx_older'
                """
            ).fetchone()[0]
        self.assertEqual(1, link_count)

    def test_transaction_detail_api_returns_json_errors_for_invalid_ids(self):
        for path, expected_status, expected_error in (
            ("/api/transactions/", 400, "Transaktions-ID fehlt."),
            (
                "/api/transactions/transaktion_unbekannt",
                404,
                "Transaktion nicht gefunden.",
            ),
        ):
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as raised:
                    urlopen(self.base_url + path, timeout=5)
                self.assertEqual(expected_status, raised.exception.code)
                self.assertEqual(
                    {"error": expected_error},
                    json.load(raised.exception),
                )

    def test_transaction_link_api_rejects_invalid_requests_without_changes(self):
        endpoint = self.base_url + "/api/transactions/tx_newer/vorgaenge"
        invalid_requests = (
            (b"{}", 400, "Das Feld vorgangs_id ist erforderlich."),
            (
                json.dumps({
                    "vorgangs_id": "vorgang_tx_older",
                    "extra": True,
                }).encode("utf-8"),
                400,
                "Das Feld vorgangs_id ist erforderlich.",
            ),
            (
                json.dumps({"vorgangs_id": "   "}).encode("utf-8"),
                400,
                "Das Feld vorgangs_id muss eine nichtleere ID enthalten.",
            ),
            (
                json.dumps({"vorgangs_id": None}).encode("utf-8"),
                400,
                "Das Feld vorgangs_id muss eine nichtleere ID enthalten.",
            ),
            (
                json.dumps({"vorgangs_id": 123}).encode("utf-8"),
                400,
                "Das Feld vorgangs_id muss eine nichtleere ID enthalten.",
            ),
            (b"{", 400, "Ung\u00fcltiger JSON-Inhalt."),
        )

        for body, expected_status, expected_error in invalid_requests:
            with self.subTest(body=body):
                request = Request(
                    endpoint,
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(HTTPError) as raised:
                    urlopen(request, timeout=5)
                self.assertEqual(expected_status, raised.exception.code)
                self.assertEqual(
                    {"error": expected_error},
                    json.load(raised.exception),
                )

                with closing(connect_database(
                    self.server.data_store.database_path
                )) as connection:
                    link_count = connection.execute(
                        """
                        SELECT COUNT(*)
                        FROM transaktion_vorgaenge
                        WHERE transaktions_id = 'tx_newer'
                          AND vorgangs_id = 'vorgang_tx_older'
                        """
                    ).fetchone()[0]
                self.assertEqual(0, link_count)

        for transaction_id, vorgangs_id, expected_error in (
            ("tx_unbekannt", "vorgang_tx_older", "Transaktion nicht gefunden."),
            ("tx_newer", "vorgang_unbekannt", "Vorgang wurde nicht gefunden."),
        ):
            with self.subTest(
                transaction_id=transaction_id,
                vorgangs_id=vorgangs_id,
            ):
                request = Request(
                    self.base_url
                    + f"/api/transactions/{transaction_id}/vorgaenge",
                    data=json.dumps({"vorgangs_id": vorgangs_id}).encode(
                        "utf-8"
                    ),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(HTTPError) as raised:
                    urlopen(request, timeout=5)
                self.assertEqual(404, raised.exception.code)
                self.assertEqual(
                    {"error": expected_error},
                    json.load(raised.exception),
                )

                with closing(connect_database(
                    self.server.data_store.database_path
                )) as connection:
                    total_links = connection.execute(
                        "SELECT COUNT(*) FROM transaktion_vorgaenge"
                    ).fetchone()[0]
                self.assertEqual(2, total_links)

    def test_classification_can_be_updated_over_http(self):
        request = Request(
            self.base_url + "/api/transactions/tx_newer/classification",
            data=json.dumps(
                {
                    "transaktionstyp": "Vergütung",
                    "oberkategorie": "Personal",
                    "unterkategorie": "Trainer",
                    "sphaere": "Ideeller Bereich",
                    "fachliche_beschreibung": "Monatsvergütung",
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 200)
            payload = json.load(response)

        self.assertEqual(
            payload["transaction"]["klassifikationsstatus"],
            "vollstaendig_klassifiziert",
        )
        self.assertEqual(payload["vorgaenge"][0]["status"], "abgeschlossen")

    def test_classification_http_rejects_invalid_payloads_without_changes(self):
        endpoint = self.base_url + "/api/transactions/tx_newer/classification"
        with urlopen(
            self.base_url + "/api/transactions/tx_newer",
            timeout=5,
        ) as response:
            original = json.load(response)["transaction"]
        classification_fields = (
            "transaktionstyp",
            "oberkategorie",
            "unterkategorie",
            "sphaere",
            "fachliche_beschreibung",
            "klassifikationsstatus",
        )
        expected_classification = {
            field: original[field] for field in classification_fields
        }
        expected_vorgang_status = self.server.data_store.vorgang_detail(
            "vorgang_tx_newer"
        )["status"]
        invalid_payloads = (
            ({}, "Mindestens ein Klassifikationsfeld"),
            (
                {
                    "oberkategorie": "Wuerde sonst gespeichert",
                    "unbekanntes_feld": "nicht erlaubt",
                },
                "Unbekannte Klassifikationsfelder: unbekanntes_feld",
            ),
            (
                {"oberkategorie": 123},
                "Das Feld oberkategorie muss Text enthalten.",
            ),
            (
                {"oberkategorie": "x" * 2001},
                "Das Feld oberkategorie darf h\u00f6chstens 2000 "
                "Zeichen enthalten.",
            ),
        )

        for payload, expected_error in invalid_payloads:
            with self.subTest(payload=payload):
                request = Request(
                    endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="PATCH",
                )
                with self.assertRaises(HTTPError) as raised:
                    urlopen(request, timeout=5)
                self.assertEqual(raised.exception.code, 400)
                self.assertIn(
                    expected_error,
                    json.load(raised.exception)["error"],
                )

                with urlopen(
                    self.base_url + "/api/transactions/tx_newer",
                    timeout=5,
                ) as response:
                    unchanged = json.load(response)["transaction"]
                self.assertEqual(
                    {field: unchanged[field] for field in classification_fields},
                    expected_classification,
                )
                self.assertEqual(
                    self.server.data_store.vorgang_detail(
                        "vorgang_tx_newer"
                    )["status"],
                    expected_vorgang_status,
                )

    def test_classification_http_returns_json_404_for_unknown_transaction(self):
        request = Request(
            self.base_url + "/api/transactions/tx_missing/classification",
            data=json.dumps({"oberkategorie": "Personal"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )

        with self.assertRaises(HTTPError) as raised:
            urlopen(request, timeout=5)

        self.assertEqual(raised.exception.code, 404)
        self.assertEqual(
            json.load(raised.exception),
            {"error": "Transaktion nicht gefunden."},
        )

    def test_vorgang_status_can_be_updated_over_http(self):
        request = Request(
            self.base_url + "/api/vorgaenge/vorgang_tx_newer/status",
            data=json.dumps({"completed": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)

        self.assertEqual(payload["vorgang"]["status"], "abgeschlossen")
        self.assertTrue(payload["vorgang"]["status_manuell"])

        request = Request(
            self.base_url + "/api/vorgaenge/vorgang_tx_newer/status",
            data=json.dumps({"completed": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)

        self.assertEqual(payload["vorgang"]["status"], "in_bearbeitung")
        self.assertTrue(payload["vorgang"]["status_manuell"])

    def test_vorgang_completion_rejects_incomplete_transaction_over_http(self):
        classification_request = Request(
            self.base_url + "/api/transactions/tx_newer/classification",
            data=json.dumps({"oberkategorie": ""}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(classification_request, timeout=5):
            pass

        request = Request(
            self.base_url + "/api/vorgaenge/vorgang_tx_newer/status",
            data=json.dumps({"completed": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )

        with self.assertRaises(HTTPError) as raised:
            urlopen(request, timeout=5)

        self.assertEqual(raised.exception.code, 400)
        payload = json.load(raised.exception)
        self.assertIn("Oberkategorie", payload["error"])

    def test_overview_vorgang_and_termine_are_available_over_http(self):
        with urlopen(self.base_url + "/api/overview", timeout=5) as response:
            overview = json.load(response)
        self.assertEqual(2, overview["counts"]["open_vorgaenge"])
        self.assertIn("unassigned_transactions", overview["counts"])
        self.assertIn("open_vorgaenge", overview["previews"])
        self.assertLessEqual(len(overview["previews"]["open_vorgaenge"]), 5)

        termin_request = Request(
            self.base_url + "/api/termine",
            data=json.dumps(
                {
                    "title": "HTTP Termin",
                    "starts_at": "2026-07-02T18:30:00+02:00",
                    "location": "Vereinsheim",
                    "vorgangs_ids": ["vorgang_tx_newer"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(termin_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            termin = json.load(response)["termin"]
        self.assertEqual(["vorgang_tx_newer"], termin["vorgangs_ids"])

        vorgang_request = Request(
            self.base_url + "/api/vorgaenge",
            data=json.dumps(
                {
                    "title": "HTTP Vorgang",
                    "description": "Über die API angelegt.",
                    "vorgangstyp": "Klärung",
                    "transaction_ids": ["tx_newer"],
                    "termin_ids": [termin["termin_id"]],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(vorgang_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            vorgang = json.load(response)["vorgang"]
        self.assertEqual("HTTP Vorgang", vorgang["titel"])
        self.assertEqual(
            [termin["termin_id"]],
            [item["termin_id"] for item in vorgang["termine"]],
        )

        update_request = Request(
            self.base_url + f"/api/vorgaenge/{vorgang['vorgangs_id']}",
            data=json.dumps(
                {"title": "HTTP Vorgang bearbeitet", "completed": False}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(update_request, timeout=5) as response:
            updated = json.load(response)["vorgang"]
        self.assertEqual("HTTP Vorgang bearbeitet", updated["titel"])

        with urlopen(self.base_url + "/api/termine", timeout=5) as response:
            termine = json.load(response)
        self.assertEqual(1, termine["count"])

        suggestions_request = Request(
            self.base_url + "/api/vorgaenge/suggestions",
            data=json.dumps(
                {"source_type": "transaction", "source_id": "tx_newer"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(suggestions_request, timeout=5) as response:
            suggestions = json.load(response)
        self.assertEqual("local_token_overlap", suggestions["strategy"])
        self.assertIn("transactions", suggestions["suggestions"])
        self.assertIn("transactions", suggestions["candidates"])

        def create_filter_test_termin(payload):
            request = Request(
                self.base_url + "/api/termine",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=5) as response:
                self.assertEqual(201, response.status)
                return json.load(response)["termin"]

        expected_filter_termin = create_filter_test_termin(
            {
                "title": "Unzugewiesener API-Zukunftstermin",
                "starts_at": "2999-01-15T18:00:00+01:00",
            }
        )
        create_filter_test_termin(
            {
                "title": "Verknuepfter API-Zukunftstermin",
                "starts_at": "2999-01-16T18:00:00+01:00",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )
        create_filter_test_termin(
            {
                "title": "Vergangener API-Termin",
                "starts_at": "2000-01-15T18:00:00+01:00",
            }
        )
        create_filter_test_termin(
            {
                "title": "Abgeschlossener API-Zukunftstermin",
                "starts_at": "2999-01-17T18:00:00+01:00",
                "status": TERMIN_STATUS_COMPLETED,
            }
        )
        create_filter_test_termin(
            {
                "title": "Abgesagter API-Zukunftstermin",
                "starts_at": "2999-01-18T18:00:00+01:00",
                "status": TERMIN_STATUS_CANCELLED,
            }
        )
        with urlopen(
            self.base_url + "/api/termine?unassigned_upcoming=true",
            timeout=5,
        ) as response:
            filtered_termine = json.load(response)
        self.assertEqual(1, filtered_termine["count"])
        self.assertEqual(
            [expected_filter_termin["termin_id"]],
            [termin["termin_id"] for termin in filtered_termine["termine"]],
        )

        with urlopen(
            self.base_url + "/api/vorgaenge/link-candidates",
            timeout=5,
        ) as response:
            candidates = json.load(response)
        self.assertIn("transactions", candidates["candidates"])

        with urlopen(
            self.base_url + "/api/transactions/period",
            timeout=5,
        ) as response:
            period = json.load(response)
        self.assertTrue(period["available"])

    def test_termin_api_rejects_invalid_data_without_partial_changes(self):
        def request_error(method, path, payload=None):
            request = Request(
                self.base_url + path,
                data=(
                    json.dumps(payload).encode("utf-8")
                    if payload is not None
                    else None
                ),
                headers={"Content-Type": "application/json"},
                method=method,
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)
            return raised.exception.code, json.load(raised.exception)

        invalid_creations = (
            ({"starts_at": "2026-07-05"}, "Titel"),
            ({"title": "Ohne Beginn"}, "Beginn"),
            (
                {"title": "Defektes Datum", "starts_at": "2026-07-05xyz"},
                "ISO-Datum",
            ),
            (
                {
                    "title": "Falscher Status",
                    "starts_at": "2026-07-05",
                    "status": "verschoben",
                },
                "Terminstatus",
            ),
            (
                {
                    "title": "Leerer Status",
                    "starts_at": "2026-07-05",
                    "status": "",
                },
                "Terminstatus",
            ),
            (
                {
                    "title": "Unbekannter Vorgang",
                    "starts_at": "2026-07-05",
                    "vorgangs_ids": ["vorgang_unbekannt"],
                },
                "Vorgang wurde nicht gefunden",
            ),
        )
        for payload, expected_error in invalid_creations:
            with self.subTest(payload=payload):
                status, response = request_error("POST", "/api/termine", payload)
                self.assertIn(status, (400, 404))
                self.assertIn(expected_error, response["error"])
                self.assertEqual([], self.server.data_store.list_termine())

        create_request = Request(
            self.base_url + "/api/termine",
            data=json.dumps(
                {
                    "title": "Unveraenderter Termin",
                    "starts_at": "2026-07-05T18:00:00+02:00",
                    "ends_at": "2026-07-05T19:00:00+02:00",
                    "vorgangs_ids": ["vorgang_tx_newer"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(create_request, timeout=5) as response:
            termin = json.load(response)["termin"]

        invalid_updates = (
            ({"ends_at": "2026-07-05T17:00:00+02:00"}, 400),
            ({"status": "unbekannt"}, 400),
            ({"vorgangs_ids": ["vorgang_unbekannt"]}, 404),
        )
        for payload, expected_status in invalid_updates:
            with self.subTest(payload=payload):
                status, response = request_error(
                    "PATCH", f"/api/termine/{termin['termin_id']}", payload
                )
                self.assertEqual(expected_status, status)
                self.assertIn("error", response)
                persisted = self.server.data_store.termin_detail(
                    termin["termin_id"]
                )
                self.assertEqual(termin, persisted)

        status, response = request_error(
            "DELETE", "/api/termine/termin_unbekannt"
        )
        self.assertEqual(404, status)
        self.assertEqual({"error": "Termin wurde nicht gefunden."}, response)
        self.assertEqual(
            termin,
            self.server.data_store.termin_detail(termin["termin_id"]),
        )

    def test_link_candidates_endpoint_reflects_new_transactions(self):
        with urlopen(
            self.base_url + "/api/vorgaenge/link-candidates",
            timeout=5,
        ) as response:
            first_payload = json.load(response)

        self.assertNotIn(
            "tx_after_start",
            [
                item["id"]
                for item in first_payload["candidates"]["transactions"]
            ],
        )

        database_path = self.server.data_store.database_path
        with closing(connect_database(database_path)) as connection:
            connection.execute(
                """
                INSERT INTO transactions (
                    transaction_id, fingerprint, occurrence, provider,
                    account_id, account_name, account_number, booking_date,
                    value_date, counterparty, amount, currency, booking_text,
                    purpose, amount_minor, counterparty_account, creditor_id,
                    mandate_reference, source_info, raw_fields_json,
                    first_seen_at, transaction_type, top_category,
                    sub_category, sphere, professional_description,
                    account_balance_minor
                ) VALUES (
                    'tx_after_start', 'fp_after_start', 1, 'testbank',
                    'acct_test', 'Hauptkonto', 'DE001', '2026-07-10',
                    '2026-07-10', 'Frischer Import', '19.20', 'EUR',
                    'Ueberweisung', 'Nach Dashboard-Start importiert', 1920,
                    'DE003', 'creditor_2', 'mandate_2', 'Testquelle',
                    '{}', '2026-07-10T08:00:00+00:00', 'Einnahme',
                    'Mitgliedschaft', 'Beitrag', 'Ideeller Bereich',
                    'Frisch importierte Kontobewegung', 4420
                )
                """
            )
            connection.commit()

        with urlopen(
            self.base_url + "/api/vorgaenge/link-candidates",
            timeout=5,
        ) as response:
            second_payload = json.load(response)

        transaction_ids = [
            item["id"]
            for item in second_payload["candidates"]["transactions"]
        ]
        self.assertIn("tx_after_start", transaction_ids)

    def test_vorgang_can_be_created_completed_over_http(self):
        request = Request(
            self.base_url + "/api/vorgaenge",
            data=json.dumps(
                {
                    "title": "HTTP Direktabschluss",
                    "description": "Mit vorhandener Transaktion.",
                    "vorgangstyp": "Ausgabe",
                    "completed": True,
                    "transaction_ids": ["tx_newer"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            self.assertEqual(201, response.status)
            vorgang = json.load(response)["vorgang"]

        self.assertEqual("abgeschlossen", vorgang["status"])
        self.assertTrue(vorgang["status_manuell"])
        self.assertEqual(
            ["tx_newer"],
            [item["transaktions_id"] for item in vorgang["transaktionen"]],
        )

    def test_completed_vorgang_creation_rejects_incomplete_transaction_over_http(self):
        self.server.data_store.update_transaction_classification(
            "tx_newer",
            {"unterkategorie": ""},
        )
        before = len(
            self.server.data_store.list_vorgaenge(
                search="HTTP Direktabschluss blockiert"
            )
        )
        request = Request(
            self.base_url + "/api/vorgaenge",
            data=json.dumps(
                {
                    "title": "HTTP Direktabschluss blockiert",
                    "completed": True,
                    "transaction_ids": ["tx_newer"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with self.assertRaises(HTTPError) as context:
            urlopen(request, timeout=5)

        self.assertEqual(400, context.exception.code)
        payload = json.loads(context.exception.read().decode("utf-8"))
        self.assertIn("Unterkategorie", payload["error"])
        self.assertEqual(
            before,
            len(
                self.server.data_store.list_vorgaenge(
                    search="HTTP Direktabschluss blockiert"
                )
            ),
        )

    def test_mail_vorgang_link_api_returns_details_and_is_idempotent(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]
        vorgangs_id = self.server.data_store.list_vorgaenge()[0]["vorgangs_id"]
        link_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgaenge",
            data=json.dumps({"vorgangs_id": vorgangs_id}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(link_request, timeout=5) as response:
            first_payload = json.load(response)

        duplicate_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgaenge",
            data=json.dumps({"vorgangs_id": vorgangs_id}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(duplicate_request, timeout=5) as response:
            duplicate_payload = json.load(response)

        self.assertEqual([vorgangs_id], first_payload["vorgangs_ids"])
        self.assertEqual([vorgangs_id], duplicate_payload["vorgangs_ids"])
        self.assertEqual(1, len(duplicate_payload["vorgaenge"]))
        self.assertEqual(
            vorgangs_id,
            duplicate_payload["vorgaenge"][0]["vorgangs_id"],
        )
        self.assertIn("titel", duplicate_payload["vorgaenge"][0])
        self.assertIn("status", duplicate_payload["vorgaenge"][0])

        unlink_request = Request(
            self.base_url
            + f"/api/mail/{inbox_id}/vorgaenge/{vorgangs_id}",
            method="DELETE",
        )
        with urlopen(unlink_request, timeout=5) as response:
            unlinked_payload = json.load(response)

        self.assertEqual([], unlinked_payload["vorgangs_ids"])
        self.assertEqual([], unlinked_payload["vorgaenge"])

    def test_mail_reply_api_accepts_recipients_and_preserves_newlines(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]
        reply_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/reply",
            data=json.dumps(
                {
                    "body": "Hallo\n\nDanke.",
                    "to_recipients": [
                        "vorstand@example.test",
                        "kasse@example.test",
                    ],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(reply_request, timeout=5) as response:
            payload = json.load(response)

        self.assertTrue(payload["sent"])
        self.assertEqual(
            ["vorstand@example.test", "kasse@example.test"],
            payload["to_recipients"],
        )
        self.assertEqual(
            {
                "body": "Hallo\n\nDanke.",
                "to_recipients": [
                    "vorstand@example.test",
                    "kasse@example.test",
                ],
            },
            self.server.mail_manager.backend.message["lastReply"],
        )

    def test_mail_analysis_and_confirmed_import_create_entities_over_http(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            mail_payload = json.load(response)
        inbox_id = mail_payload["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis_payload = json.load(response)
        analysis = analysis_payload["analysis"]
        self.assertEqual("Rechnung Stadtwerke", analysis["vorgang"]["title"])
        self.assertEqual("rechnungen", analysis["documents"][0]["category"])

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": analysis["documents"],
                    "todos": analysis["todos"],
                    "termine": analysis["termine"],
                    "links": {"transaction_ids": ["tx_newer"]},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            imported = json.load(response)

        vorgang = imported["vorgang"]
        self.assertEqual("Rechnung Stadtwerke", vorgang["titel"])
        self.assertEqual(1, len(vorgang["mails"]))
        self.assertEqual(
            ["tx_newer"],
            [item["transaktions_id"] for item in vorgang["transaktionen"]],
        )
        self.assertEqual(2, len(imported["documents"]))
        documents_by_name = {
            Path(document["dateipfad"]).name: document
            for document in imported["documents"]
        }
        self.assertEqual(
            {"rechnung.pdf", "zahlungsziel.txt"},
            set(documents_by_name),
        )
        self.assertEqual("rechnungen", documents_by_name["rechnung.pdf"]["kategorie"])
        self.assertIn("Rechnungen", documents_by_name["rechnung.pdf"]["dateipfad"])
        self.assertEqual(
            "sonstige_dokumente",
            documents_by_name["zahlungsziel.txt"]["kategorie"],
        )
        self.assertIn(
            "Sonstige Dokumente",
            documents_by_name["zahlungsziel.txt"]["dateipfad"],
        )
        for document in imported["documents"]:
            self.assertTrue(Path(document["dateipfad"]).exists())
        self.assertEqual(1, len(imported["todos"]))
        self.assertEqual("hoch", imported["todos"][0]["priority"])
        self.assertEqual(1, len(imported["termine"]))
        self.assertEqual("Termin Stadtwerke", imported["termine"][0]["title"])

    def test_mail_import_without_transaction_links_stays_successful(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": [],
                    "todos": [],
                    "termine": [],
                    "links": {},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            imported = json.load(response)

        vorgang = imported["vorgang"]
        self.assertEqual(1, len(vorgang["mails"]))
        self.assertEqual([], vorgang["transaktionen"])

    def test_mail_import_creates_manual_todo_without_analysis_suggestions(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]
        analysis["todos"] = []

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": [],
                    "todos": [
                        {
                            "enabled": True,
                            "title": "Manuell nachfassen",
                            "description": "Ohne Analysevorschlag erfasst.",
                            "due_date": "2026-07-15",
                            "priority": "hoch",
                        },
                        {
                            "enabled": True,
                            "title": "   ",
                            "description": "Leere Zeile ignorieren.",
                            "due_date": "",
                            "priority": "normal",
                        },
                    ],
                    "termine": [],
                    "links": {},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            imported = json.load(response)

        self.assertEqual(1, len(imported["todos"]))
        todo = imported["todos"][0]
        self.assertEqual("Manuell nachfassen", todo["title"])
        self.assertEqual("hoch", todo["priority"])
        self.assertEqual([imported["vorgang"]["vorgangs_id"]], todo["vorgangs_ids"])
        self.assertEqual(
            [todo["todo_id"]],
            [item["todo_id"] for item in imported["vorgang"]["todos"]],
        )

    def test_mail_import_rejects_unknown_transaction_link(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": [],
                    "todos": [],
                    "termine": [],
                    "links": {"transaction_ids": ["tx_missing"]},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(import_request, timeout=5)

        self.assertEqual(404, context.exception.code)
        payload = json.loads(context.exception.read().decode("utf-8"))
        self.assertIn("Transaktion wurde nicht gefunden", payload["error"])
        self.assertIn("tx_missing", payload["error"])

    def test_mail_import_can_complete_new_vorgang_over_http(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]
        analysis["vorgang"]["completed"] = True

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": analysis["documents"],
                    "todos": [],
                    "termine": [],
                    "links": {"transaction_ids": ["tx_newer"]},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            imported = json.load(response)

        vorgang = imported["vorgang"]
        self.assertEqual("abgeschlossen", vorgang["status"])
        self.assertTrue(vorgang["status_manuell"])
        self.assertTrue(vorgang["abschluss_moeglich"])
        self.assertEqual(
            {
                "requested": True,
                "completed": True,
                "rejected": False,
                "message": "Vorgang direkt abgeschlossen.",
            },
            imported["direct_completion"],
        )
        self.assertEqual(2, len(imported["documents"]))
        self.assertEqual(["tx_newer"], [
            item["transaktions_id"] for item in vorgang["transaktionen"]
        ])

    def test_mail_import_applies_inline_classification_before_completion(self):
        self.server.data_store.update_transaction_classification(
            "tx_newer",
            {
                "transaktionstyp": "",
                "oberkategorie": "",
                "unterkategorie": "",
                "sphaere": "",
            },
        )
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]
        analysis["vorgang"]["completed"] = True

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": analysis["documents"],
                    "todos": [],
                    "termine": [],
                    "links": {"transaction_ids": ["tx_newer"]},
                    "transaction_classifications": [
                        {
                            "transaction_id": "tx_newer",
                            "transaktionstyp": "Ausgabe",
                            "oberkategorie": "Betrieb",
                            "unterkategorie": "Energie",
                            "sphaere": "Zweckbetrieb",
                            "fachliche_beschreibung": "Stromrechnung",
                        }
                    ],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            imported = json.load(response)

        self.assertEqual("abgeschlossen", imported["vorgang"]["status"])
        self.assertEqual(
            {
                "requested": True,
                "completed": True,
                "rejected": False,
                "message": "Vorgang direkt abgeschlossen.",
            },
            imported["direct_completion"],
        )
        transaction = self.server.data_store.transaction_detail("tx_newer")
        self.assertEqual("Ausgabe", transaction["transaktionstyp"])
        self.assertEqual("Betrieb", transaction["oberkategorie"])
        self.assertEqual("Energie", transaction["unterkategorie"])
        self.assertEqual("Zweckbetrieb", transaction["sphaere"])
        self.assertEqual(
            "Stromrechnung",
            transaction["fachliche_beschreibung"],
        )

    def test_mail_import_rejects_invalid_inline_classification_without_partial_state(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": analysis["documents"],
                    "todos": [],
                    "termine": [],
                    "links": {"transaction_ids": ["tx_newer"]},
                    "transaction_classifications": [
                        {
                            "transaction_id": "tx_newer",
                            "transaktionstyp": "Ausgabe",
                            "unbekannt": "Wert",
                        }
                    ],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(import_request, timeout=5)

        self.assertEqual(400, context.exception.code)
        payload = json.loads(context.exception.read().decode("utf-8"))
        self.assertIn("Unbekannte Klassifikationsfelder", payload["error"])
        with urlopen(
            self.base_url + f"/api/mail/{inbox_id}/vorgaenge",
            timeout=5,
        ) as response:
            linked_payload = json.load(response)
        self.assertEqual([], linked_payload["vorgangs_ids"])
        transaction = self.server.data_store.transaction_detail("tx_newer")
        self.assertEqual("Spielbetrieb", transaction["oberkategorie"])

    def test_mail_import_completion_returns_blocker_over_http(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]

        analysis_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-analysis",
            data=b"",
            method="POST",
        )
        with urlopen(analysis_request, timeout=5) as response:
            analysis = json.load(response)["analysis"]
        analysis["vorgang"]["completed"] = True

        import_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/vorgang-import",
            data=json.dumps(
                {
                    "vorgang": analysis["vorgang"],
                    "documents": [],
                    "todos": [],
                    "termine": [],
                    "links": {"transaction_ids": ["tx_newer"]},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(import_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            payload = json.load(response)

        self.assertEqual("in_bearbeitung", payload["vorgang"]["status"])
        self.assertEqual(
            {
                "requested": True,
                "completed": False,
                "rejected": True,
                "message": (
                    "Vorgaenge vom Typ Rechnung brauchen vor dem Abschluss "
                    "mindestens ein verknuepftes Dokument."
                ),
            },
            payload["direct_completion"],
        )

        with urlopen(
            self.base_url + f"/api/mail/{inbox_id}/vorgaenge",
            timeout=5,
        ) as response:
            linked_payload = json.load(response)

        self.assertEqual(1, len(linked_payload["vorgangs_ids"]))
        persisted_id = linked_payload["vorgangs_ids"][0]
        persisted = self.server.data_store.vorgang_detail(persisted_id)
        self.assertIsNotNone(persisted)
        self.assertEqual("in_bearbeitung", persisted["status"])
        self.assertFalse(persisted["status_manuell"])
        self.assertFalse(persisted["abschluss_moeglich"])
        self.assertIn(
            "mindestens ein verknuepftes Dokument",
            " ".join(persisted["abschluss_blocker"]),
        )

    def test_todo_crud_and_vorgang_links_are_available_over_http(self):
        create_request = Request(
            self.base_url + "/api/todos",
            data=json.dumps(
                {
                    "title": "HTTP To-Do",
                    "description": "Über die API angelegt.",
                    "due_date": "2026-07-01",
                    "priority": "hoch",
                    "vorgangs_ids": ["vorgang_tx_newer"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(create_request, timeout=5) as response:
            self.assertEqual(201, response.status)
            todo = json.load(response)["todo"]
        todo_id = todo["todo_id"]
        self.assertEqual(["vorgang_tx_newer"], todo["vorgangs_ids"])

        with urlopen(self.base_url + "/api/todos", timeout=5) as response:
            listed = json.load(response)
        self.assertEqual(1, listed["count"])

        update_request = Request(
            self.base_url + f"/api/todos/{todo_id}",
            data=json.dumps({"completed": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(update_request, timeout=5) as response:
            self.assertTrue(json.load(response)["todo"]["completed"])

        link_request = Request(
            self.base_url + f"/api/todos/{todo_id}/vorgaenge",
            data=json.dumps(
                {"vorgangs_id": "vorgang_tx_older"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(link_request, timeout=5) as response:
            linked = json.load(response)["todo"]["vorgangs_ids"]
        self.assertEqual(
            ["vorgang_tx_newer", "vorgang_tx_older"],
            linked,
        )

        unlink_request = Request(
            self.base_url
            + f"/api/todos/{todo_id}/vorgaenge/vorgang_tx_newer",
            method="DELETE",
        )
        with urlopen(unlink_request, timeout=5) as response:
            self.assertEqual(
                ["vorgang_tx_older"],
                json.load(response)["todo"]["vorgangs_ids"],
            )

        delete_request = Request(
            self.base_url + f"/api/todos/{todo_id}",
            method="DELETE",
        )
        with urlopen(delete_request, timeout=5) as response:
            self.assertTrue(json.load(response)["deleted"])

    def test_todo_create_rejects_invalid_payloads_with_json_error(self):
        invalid_payloads = (
            {"title": "Unbekanntes Feld", "unexpected": True},
            {"title": "Ungueltige Prioritaet", "priority": "sofort"},
            {"title": "Ungueltiges Datum", "due_date": "morgen"},
            {"title": "Ungueltige Links", "vorgangs_ids": "vorgang_tx_newer"},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                request = Request(
                    self.base_url + "/api/todos",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)

                self.assertEqual(400, caught.exception.code)
                error_payload = json.loads(
                    caught.exception.read().decode("utf-8")
                )
                self.assertIsInstance(error_payload.get("error"), str)
                self.assertTrue(error_payload["error"])

        with urlopen(self.base_url + "/api/todos", timeout=5) as response:
            self.assertEqual(0, json.load(response)["count"])

    def test_todo_patch_rejects_invalid_payloads_without_changes(self):
        todo = self.server.data_store.create_todo(
            {
                "title": "Unveraendertes To-Do",
                "description": "Ausgangszustand",
                "priority": "normal",
                "due_date": "2026-07-01",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )
        invalid_payloads = (
            {"unexpected": True},
            {"priority": "sofort"},
            {"due_date": "morgen"},
            {"vorgangs_ids": "vorgang_tx_older"},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                request = Request(
                    self.base_url + f"/api/todos/{todo['todo_id']}",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="PATCH",
                )
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)

                self.assertEqual(400, caught.exception.code)
                error_payload = json.loads(
                    caught.exception.read().decode("utf-8")
                )
                self.assertIsInstance(error_payload.get("error"), str)

        persisted = self.server.data_store.todo_detail(todo["todo_id"])
        self.assertEqual(todo, persisted)

    def test_unknown_todo_references_return_404_without_partial_state(self):
        create_request = Request(
            self.base_url + "/api/todos",
            data=json.dumps(
                {
                    "title": "Nicht anlegen",
                    "vorgangs_ids": ["vorgang_missing"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as create_error:
            urlopen(create_request, timeout=5)
        self.assertEqual(404, create_error.exception.code)
        self.assertTrue(
            json.loads(create_error.exception.read().decode("utf-8"))["error"]
        )
        self.assertEqual([], self.server.data_store.list_todos())

        todo = self.server.data_store.create_todo(
            {
                "title": "Bestehendes To-Do",
                "vorgangs_ids": ["vorgang_tx_newer"],
            }
        )
        patch_request = Request(
            self.base_url + f"/api/todos/{todo['todo_id']}",
            data=json.dumps(
                {
                    "title": "Darf nicht gespeichert werden",
                    "vorgangs_ids": ["vorgang_missing"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with self.assertRaises(HTTPError) as patch_error:
            urlopen(patch_request, timeout=5)
        self.assertEqual(404, patch_error.exception.code)
        self.assertTrue(
            json.loads(patch_error.exception.read().decode("utf-8"))["error"]
        )
        self.assertEqual(
            todo,
            self.server.data_store.todo_detail(todo["todo_id"]),
        )

    def test_missing_todo_patch_and_delete_return_404_json_error(self):
        requests = (
            Request(
                self.base_url + "/api/todos/todo_missing",
                data=json.dumps({"completed": True}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="PATCH",
            ),
            Request(
                self.base_url + "/api/todos/todo_missing",
                method="DELETE",
            ),
        )

        for request in requests:
            with self.subTest(method=request.method):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)
                self.assertEqual(404, caught.exception.code)
                error_payload = json.loads(
                    caught.exception.read().decode("utf-8")
                )
                self.assertEqual(
                    "To-Do wurde nicht gefunden.",
                    error_payload["error"],
                )

    def test_belege_catalog_and_vorgang_links_are_available_over_http(self):
        with urlopen(self.base_url + "/api/belege", timeout=5) as response:
            payload = json.load(response)
        self.assertEqual(1, payload["count"])
        self.assertTrue(payload["directory"].endswith("belege"))
        beleg = payload["belege"][0]
        self.assertEqual("beleg_1", beleg["beleg_id"])
        self.assertEqual(["vorgang_tx_newer"], beleg["vorgangs_ids"])
        with urlopen(
            self.base_url + "/api/belege?unassigned_only=true",
            timeout=5,
        ) as response:
            self.assertEqual(0, json.load(response)["count"])

        unlink_request = Request(
            self.base_url
            + "/api/belege/beleg_1/vorgaenge/vorgang_tx_newer",
            method="DELETE",
        )
        with urlopen(unlink_request, timeout=5) as response:
            self.assertEqual(
                [],
                json.load(response)["beleg"]["vorgangs_ids"],
            )
        with urlopen(
            self.base_url + "/api/belege?unassigned_only=true",
            timeout=5,
        ) as response:
            filtered = json.load(response)
        self.assertEqual(1, filtered["count"])
        self.assertEqual("beleg_1", filtered["belege"][0]["beleg_id"])

        link_request = Request(
            self.base_url + "/api/belege/beleg_1/vorgaenge",
            data=json.dumps(
                {"vorgangs_id": "vorgang_tx_older"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(link_request, timeout=5) as response:
            self.assertEqual(
                ["vorgang_tx_older"],
                json.load(response)["beleg"]["vorgangs_ids"],
            )

    def test_document_upload_can_be_saved_without_vorgang(self):
        content = b"Bestaetigung Bandenwerbung"
        request = Request(
            self.base_url + "/api/belege",
            data=json.dumps(
                {
                    "content_base64": base64.b64encode(content).decode("ascii"),
                    "filename": "bandenwerbung.txt",
                    "content_type": "text/plain",
                    "metadata": {
                        "category": "sonstige_dokumente",
                        "description": "Bestaetigung",
                    },
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(201, response.status)
            beleg = json.load(response)["beleg"]

        self.assertEqual([], beleg["vorgangs_ids"])
        self.assertEqual("sonstige_dokumente", beleg["kategorie"])
        self.assertEqual(content, Path(beleg["dateipfad"]).read_bytes())
        with urlopen(
            self.base_url + "/api/belege?unassigned_only=true", timeout=5
        ) as response:
            unassigned_ids = {
                item["beleg_id"] for item in json.load(response)["belege"]
            }
        self.assertIn(beleg["beleg_id"], unassigned_ids)

    def test_document_upload_rejects_invalid_content_without_persistence(self):
        before_files = set(self.server.data_store.belege_directory.rglob("*"))
        with closing(
            connect_database(self.server.data_store.database_path)
        ) as connection:
            before_count = connection.execute(
                "SELECT COUNT(*) FROM belege"
            ).fetchone()[0]
        request = Request(
            self.base_url + "/api/belege",
            data=json.dumps(
                {"content_base64": "not base64!", "filename": "beleg.txt"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as raised:
            urlopen(request, timeout=5)
        self.assertEqual(400, raised.exception.code)
        with closing(
            connect_database(self.server.data_store.database_path)
        ) as connection:
            self.assertEqual(
                before_count,
                connection.execute("SELECT COUNT(*) FROM belege").fetchone()[0],
            )
        self.assertEqual(
            before_files,
            set(self.server.data_store.belege_directory.rglob("*")),
        )

    def test_vorgang_api_rejects_invalid_input_without_persistence(self):
        before = len(self.server.data_store.list_vorgaenge())
        for payload, expected_error in (
            ({"title": 123}, "Das Feld title muss Text enthalten."),
            (
                {"title": "Ungueltig", "beleg_ids": [123]},
                "beleg_ids darf nur Text-IDs enthalten.",
            ),
            (
                {"title": "Ungueltig", "unbekannt": True},
                "Unbekannte Felder fuer den Vorgang.",
            ),
        ):
            with self.subTest(payload=payload):
                request = Request(
                    self.base_url + "/api/vorgaenge",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)
                self.assertEqual(400, caught.exception.code)
                self.assertEqual(
                    {"error": expected_error},
                    json.load(caught.exception),
                )
                self.assertEqual(
                    before,
                    len(self.server.data_store.list_vorgaenge()),
                )

    def test_vorgang_api_returns_404_for_unknown_update_and_delete(self):
        requests = (
            Request(
                self.base_url + "/api/vorgaenge/vorgang_missing",
                data=json.dumps({"title": "Fehlt"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="PATCH",
            ),
            Request(
                self.base_url + "/api/vorgaenge/vorgang_missing",
                method="DELETE",
            ),
        )
        for request in requests:
            with self.subTest(method=request.method):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)
                self.assertEqual(404, caught.exception.code)
                self.assertEqual(
                    {"error": "Vorgang nicht gefunden."},
                    json.load(caught.exception),
                )

    def test_beleg_link_api_rejects_invalid_links_without_changes(self):
        endpoint = self.base_url + "/api/belege/beleg_1/vorgaenge"
        for payload, status, expected_error in (
            ({"vorgangs_id": 123}, 400,
             "Das Feld vorgangs_id muss eine nichtleere ID enthalten."),
            ({"vorgangs_id": "vorgang_missing"}, 404,
             "Vorgang wurde nicht gefunden."),
        ):
            with self.subTest(payload=payload):
                request = Request(
                    endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(HTTPError) as caught:
                    urlopen(request, timeout=5)
                self.assertEqual(status, caught.exception.code)
                self.assertEqual(
                    {"error": expected_error},
                    json.load(caught.exception),
                )
                self.assertEqual(
                    ["vorgang_tx_newer"],
                    self.server.data_store.beleg_detail("beleg_1")[
                        "vorgangs_ids"
                    ],
                )

        unlink_request = Request(
            endpoint + "/vorgang_missing",
            method="DELETE",
        )
        with self.assertRaises(HTTPError) as caught:
            urlopen(unlink_request, timeout=5)
        self.assertEqual(404, caught.exception.code)
        self.assertEqual(
            {"error": "Vorgang wurde nicht gefunden."},
            json.load(caught.exception),
        )
        self.assertEqual(
            ["vorgang_tx_newer"],
            self.server.data_store.beleg_detail("beleg_1")["vorgangs_ids"],
        )

    def test_beleg_original_document_is_served_over_http(self):
        document_path = (
            self.server.data_store.database_path.parent
            / "belege"
            / "beleg_1.pdf"
        )
        document_path.parent.mkdir(exist_ok=True)
        document_path.write_bytes(b"%PDF-1.4\nTestbeleg\n")
        with closing(connect_database(self.server.data_store.database_path)) as connection:
            connection.execute(
                """
                UPDATE belege
                SET vorhanden = 1, dateigroesse = ?
                WHERE beleg_id = 'beleg_1'
                """,
                (document_path.stat().st_size,),
            )
            connection.commit()

        with urlopen(
            self.base_url + "/api/belege/beleg_1/document",
            timeout=5,
        ) as response:
            content = response.read()

        self.assertEqual(b"%PDF-1.4\nTestbeleg\n", content)
        self.assertEqual("application/pdf", response.headers["Content-Type"])
        self.assertIn(
            'inline; filename="beleg_1.pdf"',
            response.headers["Content-Disposition"],
        )

    def test_beleg_original_document_returns_404_for_unknown_beleg(self):
        with self.assertRaises(HTTPError) as context:
            urlopen(
                self.base_url + "/api/belege/beleg_missing/document",
                timeout=5,
            )
        self.assertEqual(404, context.exception.code)
        payload = json.load(context.exception)
        self.assertIn("Beleg wurde nicht gefunden", payload["error"])

    def test_beleg_original_document_returns_404_for_missing_file(self):
        with self.assertRaises(HTTPError) as context:
            urlopen(
                self.base_url + "/api/belege/beleg_1/document",
                timeout=5,
            )
        self.assertEqual(404, context.exception.code)
        payload = json.load(context.exception)
        self.assertIn(
            "Originaldokument wurde nicht gefunden",
            payload["error"],
        )

    def test_rule_creation_and_refresh_are_available_over_http(self):
        rule_request = Request(
            self.base_url + "/api/rules",
            data=json.dumps(
                {
                    "name": "HTTP-Regel",
                    "enabled": True,
                    "match_field": "purpose",
                    "match_operator": "contains",
                    "match_value": "Unbekannter Wert",
                    "transaction_type": "Ausgabe",
                    "top_category": "HTTP",
                    "sub_category": "Test",
                    "sphere": "Ideeller Bereich",
                    "professional_description": "HTTP-Test",
                    "apply_now": True,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(rule_request, timeout=5) as response:
            payload = json.load(response)
            self.assertEqual(response.status, 201)
            self.assertEqual(payload["rule"]["name"], "HTTP-Regel")
            rule_id = payload["rule"]["rule_id"]

        update_request = Request(
            self.base_url + f"/api/rules/{rule_id}",
            data=json.dumps(
                {
                    "name": "HTTP-Regel geändert",
                    "enabled": False,
                    "match_field": "counterparty",
                    "match_operator": "equals",
                    "match_value": "Neuer Verein",
                    "transaction_type": "Einnahme",
                    "top_category": "HTTP",
                    "sub_category": "Bearbeitet",
                    "sphere": "Zweckbetrieb",
                    "professional_description": "Geändert",
                    "apply_now": False,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(update_request, timeout=5) as response:
            payload = json.load(response)
            self.assertFalse(payload["rule"]["enabled"])
            self.assertEqual(payload["rule"]["rule_id"], rule_id)

        with urlopen(
            self.base_url + "/api/rules?search=Bearbeitet",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertEqual(
                [rule["rule_id"] for rule in payload["rules"]],
                [rule_id],
            )

        refresh_request = Request(
            self.base_url + "/api/refresh",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(refresh_request, timeout=5) as response:
            self.assertEqual(response.status, 202)
        for _ in range(20):
            with urlopen(self.base_url + "/api/refresh", timeout=5) as response:
                payload = json.load(response)
            if payload["status"] != "running":
                break
            threading.Event().wait(0.01)
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["result"]["new_transactions"], 2)

    def test_rule_can_be_deleted_over_http(self):
        create_request = Request(
            self.base_url + "/api/rules",
            data=json.dumps(
                {
                    "name": "HTTP-Vorgangsregel",
                    "enabled": True,
                    "match_field": "purpose",
                    "match_operator": "equals",
                    "match_value": "Neuer Zweck",
                    "transaction_type": "Vergütung",
                    "top_category": "HTTP",
                    "sub_category": "Vorgang",
                    "sphere": "Ideeller Bereich",
                    "professional_description": "",
                    "apply_now": False,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(create_request, timeout=5) as response:
            rule_id = json.load(response)["rule"]["rule_id"]

        delete_request = Request(
            self.base_url + f"/api/rules/{rule_id}",
            method="DELETE",
        )
        with urlopen(delete_request, timeout=5) as response:
            payload = json.load(response)
        self.assertEqual(payload["deleted_rule_id"], rule_id)

        with urlopen(self.base_url + "/api/rules", timeout=5) as response:
            payload = json.load(response)
        self.assertNotIn(
            rule_id,
            [rule["rule_id"] for rule in payload["rules"]],
        )

    def test_completion_rules_are_available_over_http(self):
        create_request = Request(
            self.base_url + "/api/completion-rules",
            data=json.dumps(
                {
                    "name": "HTTP-Abschlussregel",
                    "enabled": True,
                    "conditions": [
                        {
                            "connector": "",
                            "match_field": "top_category",
                            "match_operator": "equals",
                            "match_value": "Spielbetrieb",
                        }
                    ],
                    "apply_now": True,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(create_request, timeout=5) as response:
            self.assertEqual(response.status, 201)
            created = json.load(response)
        rule_id = created["rule"]["rule_id"]
        self.assertGreaterEqual(created["changed_vorgaenge"], 1)

        with urlopen(
            self.base_url + "/api/completion-rules?search=HTTP",
            timeout=5,
        ) as response:
            listed = json.load(response)
        self.assertEqual(
            [rule["rule_id"] for rule in listed["rules"]],
            [rule_id],
        )

        update_request = Request(
            self.base_url + f"/api/completion-rules/{rule_id}",
            data=json.dumps(
                {
                    "name": "HTTP-Abschlussregel deaktiviert",
                    "enabled": False,
                    "match_field": "top_category",
                    "match_operator": "equals",
                    "match_value": "Spielbetrieb",
                    "apply_now": True,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(update_request, timeout=5) as response:
            updated = json.load(response)
        self.assertFalse(updated["rule"]["enabled"])

        delete_request = Request(
            self.base_url + f"/api/completion-rules/{rule_id}",
            method="DELETE",
        )
        with urlopen(delete_request, timeout=5) as response:
            deleted = json.load(response)
        self.assertEqual(deleted["deleted_rule_id"], rule_id)

    def test_unknown_transaction_returns_not_found(self):
        with self.assertRaises(HTTPError) as raised:
            urlopen(
                self.base_url + "/api/transactions/tx_unknown",
                timeout=5,
            )

        self.assertEqual(raised.exception.code, 404)

    def test_player_premium_task_is_available_over_http(self):
        with urlopen(
            self.base_url + "/api/player-premiums",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertTrue(payload["available"])
            self.assertEqual(payload["seasons"][-1], "2022/2023")
            self.assertEqual(
                [team["team_id"] for team in payload["teams"]],
                ["herren_1", "herren_2", "damen"],
            )

        request = Request(
            self.base_url + "/api/player-premiums",
            data=json.dumps(
                {
                    "season": "2025/2026",
                    "team_ids": ["herren_1"],
                    "point_values": {"herren_1": "6.50"},
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 202)
        for _ in range(20):
            with urlopen(
                self.base_url + "/api/player-premiums",
                timeout=5,
            ) as response:
                payload = json.load(response)
            if payload["status"] != "running":
                break
            threading.Event().wait(0.01)

        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["result"]["season"], "2025/2026")
        self.assertEqual(
            payload["result"]["teams"][0]["team_id"],
            "herren_1",
        )
        self.assertEqual(
            payload["result"]["teams"][0]["point_value"],
            6.5,
        )

    def test_player_payment_review_is_available_over_http(self):
        with urlopen(
            self.base_url + "/api/player-premium-payments",
            timeout=5,
        ) as response:
            payload = json.load(response)
            self.assertTrue(payload["available"])
            self.assertEqual(payload["status"], "idle")

        request = Request(
            self.base_url + "/api/player-premium-payments",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 202)
        for _ in range(20):
            with urlopen(
                self.base_url + "/api/player-premium-payments",
                timeout=5,
            ) as response:
                payload = json.load(response)
            if payload["status"] != "running":
                break
            threading.Event().wait(0.01)

        self.assertEqual(payload["status"], "completed")
        self.assertEqual(
            payload["result"]["players"][0]["masked_iban"],
            "DE89 **** **** **** **30 00",
        )
        self.assertNotIn(
            "DE89370400440532013000",
            json.dumps(payload),
        )

    def test_player_payment_can_be_entered_manually_over_http(self):
        full_iban = "DE89370400440532013000"
        request = Request(
            self.base_url
            + "/api/player-premium-payments/Max%20Mustermann",
            data=json.dumps(
                {
                    "account_holder": "Max Mustermann",
                    "iban": full_iban,
                    "bic": "COBADEFFXXX",
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )

        with urlopen(request, timeout=5) as response:
            payload = json.load(response)

        self.assertTrue(payload["manual_available"])
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(
            self.player_payment_updates,
            [
                (
                    "Max Mustermann",
                    {
                        "account_holder": "Max Mustermann",
                        "iban": full_iban,
                        "bic": "COBADEFFXXX",
                    },
                )
            ],
        )
        self.assertNotIn(full_iban, json.dumps(payload))
        self.assertEqual(
            payload["result"]["players"][0]["payment_source"],
            "manual",
        )


class DashboardTransactionBrowserTests(unittest.TestCase):
    def test_transaction_split_editor_updates_and_shows_errors(self):
        try:
            from playwright.sync_api import expect, sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            server = create_server(database_path, port=0)
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page_errors = []
                    page.on(
                        "pageerror",
                        lambda error: page_errors.append(str(error)),
                    )
                    page.goto(base_url, wait_until="networkidle")
                    page.locator("tr[data-id='tx_newer']").click()
                    editor = page.locator(".split-editor")
                    expect(editor).to_be_visible()
                    expect(editor).to_contain_text("Teilbetrag Eintritt")
                    vorgang_select = editor.locator("[data-split-vorgang]").first()
                    expect(vorgang_select).to_have_value("vorgang_tx_newer")
                    expect(editor).to_contain_text("Belege des Vorgangs")
                    expect(editor).to_contain_text("beleg_1.pdf")
                    expect(
                        editor.locator("[data-split-summary='original']")
                    ).to_contain_text("Originalbetrag")
                    expect(
                        editor.locator("[data-split-summary='sum']")
                    ).to_contain_text("Split-Summe")
                    expect(
                        editor.locator("[data-split-summary='difference']")
                    ).to_contain_text("Differenz")
                    expect(
                        editor.locator("[data-split-amount]").first()
                    ).to_have_value("15,00")
                    with page.expect_response(
                        lambda response: (
                            response.request.method == "GET"
                            and response.url.endswith(
                                "/api/transactions/tx_newer/splits"
                            )
                        )
                    ):
                        editor.locator(
                            "button",
                            has_text="Splits neu laden",
                        ).click()
                    expect(
                        editor.locator("[data-split-amount]").first()
                    ).to_have_value("15,00")
                    expect(editor).to_contain_text("Spielbetrieb")
                    self.assertTrue(
                        page.evaluate(
                            """
                            () => Boolean(
                              document
                                .querySelector("[data-split-type]")
                                .getAttribute("list")
                            )
                            """
                        )
                    )

                    first_row = editor.locator(".split-row").first()
                    first_top = first_row.locator("[data-split-top]")
                    first_sub = first_row.locator("[data-split-sub]")
                    first_sphere = first_row.locator("[data-split-sphere]")
                    first_top.fill("")
                    expect(first_sub).to_be_disabled()
                    first_top.fill("Spielbetrieb")
                    expect(first_sub).to_be_enabled()
                    self.assertEqual(
                        ["Eintritt"],
                        first_sub.evaluate(
                            """
                            input => [...document.getElementById(input.list.id)
                              .options].map(option => option.value)
                            """
                        ),
                    )
                    first_sphere.select_option("Vermögensverwaltung")
                    first_sub.fill("Eintritt")
                    expect(first_sphere).to_have_value(
                        "Vermögensverwaltung"
                    )

                    editor.locator("[data-split-amount]").first().fill("10,00")
                    editor.locator("button", has_text="Zeile hinzufuegen").click()
                    second_row = editor.locator(".split-row").last()
                    expect(
                        second_row.locator("[data-split-amount]")
                    ).to_have_value("15,00")
                    second_row.locator(
                        "[data-split-description]"
                    ).fill("API Teil 2")
                    second_row.locator("[data-split-type]").fill("Einnahme")
                    second_row.locator("[data-split-top]").fill("Spielbetrieb")
                    second_row.locator("[data-split-sub]").fill("Eintritt")
                    second_row.locator(
                        "[data-split-professional]"
                    ).fill("Browser-Test")
                    second_row.locator("[data-split-vorgang]").select_option(
                        "vorgang_tx_newer"
                    )
                    expect(second_row).to_contain_text("beleg_1.pdf")

                    with page.expect_response(
                        lambda response: (
                            response.request.method == "PUT"
                            and response.url.endswith(
                                "/api/transactions/tx_newer/splits"
                            )
                        )
                    ):
                        editor.locator(
                            "button",
                            has_text="Splits speichern",
                        ).click()
                    expect(editor.locator(".save-state")).to_contain_text(
                        "Gespeichert"
                    )

                    persisted = page.evaluate(
                        """
                        async () => {
                          const response = await fetch(
                            "/api/transactions/tx_newer"
                          );
                          return (await response.json()).transaction.splits;
                        }
                        """
                    )
                    self.assertEqual(
                        [1000, 1500],
                        [split["amount_minor"] for split in persisted],
                    )
                    self.assertEqual(
                        ["Teilbetrag Eintritt", "API Teil 2"],
                        [split["description"] for split in persisted],
                    )
                    self.assertEqual(
                        "Vermögensverwaltung",
                        persisted[0]["sphere"],
                    )
                    self.assertEqual(
                        ["vorgang_tx_newer", "vorgang_tx_newer"],
                        [split["vorgangs_id"] for split in persisted],
                    )

                    editor.locator("[data-split-amount]").first().fill("")
                    expect(editor.locator(".form-error")).to_contain_text(
                        "Split 1 braucht einen Betrag in Euro."
                    )
                    expect(
                        editor.locator(
                            "button",
                            has_text="Splits speichern",
                        )
                    ).to_be_disabled()

                    editor.locator("[data-split-amount]").first().fill("10,00")
                    second_row = editor.locator(".split-row").last()
                    second_row.locator("[data-split-amount]").fill("10,00")
                    with page.expect_response(
                        lambda response: (
                            response.request.method == "PUT"
                            and response.url.endswith(
                                "/api/transactions/tx_newer/splits"
                            )
                        )
                    ) as invalid_response:
                        editor.locator(
                            "button",
                            has_text="Splits speichern",
                        ).click()
                    self.assertEqual(400, invalid_response.value.status)
                    expect(editor.locator(".form-error")).to_contain_text(
                        "Summe der Splits"
                    )

                    persisted_after_error = page.evaluate(
                        """
                        async () => {
                          const response = await fetch(
                            "/api/transactions/tx_newer"
                          );
                          return (await response.json()).transaction.splits;
                        }
                        """
                    )
                    self.assertEqual(
                        [1000, 1500],
                        [
                            split["amount_minor"]
                            for split in persisted_after_error
                        ],
                    )

                    second_row.locator(
                        "button",
                        has_text="Entfernen",
                    ).click()
                    editor.locator("[data-split-amount]").first().fill("25,00")
                    with page.expect_response(
                        lambda response: (
                            response.request.method == "PUT"
                            and response.url.endswith(
                                "/api/transactions/tx_newer/splits"
                            )
                        )
                    ):
                        editor.locator(
                            "button",
                            has_text="Splits speichern",
                        ).click()
                    expect(editor.locator(".split-row")).to_have_count(1)
                    expect(
                        editor.locator("[data-split-summary='difference']")
                    ).to_contain_text("0,00")

                    persisted_after_remove = page.evaluate(
                        """
                        async () => {
                          const response = await fetch(
                            "/api/transactions/tx_newer"
                          );
                          return (await response.json()).transaction.splits;
                        }
                        """
                    )
                    self.assertEqual(
                        [2500],
                        [
                            split["amount_minor"]
                            for split in persisted_after_remove
                        ],
                    )
                    self.assertEqual([], page_errors)
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


class DashboardTodoBrowserTests(unittest.TestCase):
    def test_unassigned_documents_overview_card_click_opens_document_context(self):
        try:
            from playwright.sync_api import expect, sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            belege_directory = Path(temporary_directory) / "belege"
            belege_directory.mkdir()
            (belege_directory / "nicht-zugewiesen.pdf").write_bytes(
                b"%PDF-test"
            )
            server = create_server(
                database_path,
                port=0,
                mail_backend=FakeDashboardMailBackend(),
                mail_spam_scorer=FakeDashboardSpamScorer(),
            )
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page_errors = []
                    page.on(
                        "pageerror",
                        lambda error: page_errors.append(str(error)),
                    )
                    page.goto(base_url, wait_until="networkidle")

                    card = page.locator(
                        "[data-overview-key='unassigned_documents']"
                    )
                    expect(card).to_have_attribute(
                        "data-overview-entity",
                        "documents",
                    )
                    expect(card).to_contain_text(
                        "Nicht zugewiesene Dokumente"
                    )
                    expect(card).to_contain_text("1")

                    card.click()

                    expect(page.locator("#transaction-dialog")).to_be_visible()
                    expect(page.locator("#detail-title")).to_have_text(
                        "nicht-zugewiesen.pdf"
                    )
                    expect(
                        page.locator(
                            "[data-suggestion-field='beleg_ids'] input[type='checkbox']:checked"
                        )
                    ).to_have_count(1)
                    expect(
                        page.locator(
                            "[data-suggestion-field='beleg_ids'] .suggestion-row"
                        ).first
                    ).to_contain_text("nicht-zugewiesen.pdf")
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

    def test_overview_cards_route_to_matching_tabs_and_filters(self):
        try:
            from playwright.sync_api import expect, sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            store = DashboardDataStore(database_path)
            store.create_todo({"title": "Offene Aufgabe"})
            store.create_termin(
                {
                    "title": "Mitgliederversammlung",
                    "starts_at": "2999-01-15T18:00:00+01:00",
                }
            )
            server = create_server(
                database_path,
                port=0,
                mail_backend=FakeDashboardMailBackend(),
                mail_spam_scorer=FakeDashboardSpamScorer(),
            )
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page_errors = []
                    page.on(
                        "pageerror",
                        lambda error: page_errors.append(str(error)),
                    )
                    page.goto(base_url, wait_until="networkidle")

                    expect(page.locator(".dashboard-start")).to_be_visible()
                    expect(page.locator("#dashboard-tab")).to_have_attribute(
                        "aria-selected", "true"
                    )
                    expect(page.locator("#transactions-panel")).to_be_hidden()
                    expect(page.locator("#dashboard-refresh")).to_have_text(
                        "Alles synchronisieren"
                    )
                    expect(page.locator("#dashboard-open-vorgaenge")).to_contain_text(
                        "Neuer Verein"
                    )

                    page.locator(
                        "[data-overview-key='open_vorgaenge']"
                    ).click()
                    expect(page.locator("#vorgaenge-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator("#vorgang-hide-completed")
                    ).to_be_checked()

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='open_todos']").click()
                    expect(page.locator("#todo-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator("#todo-hide-completed")
                    ).to_be_checked()

                    page.locator("#dashboard-tab").click()
                    page.locator(
                        "[data-overview-key='unassigned_transactions']"
                    ).click()
                    expect(page.locator("#transactions-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator(
                            "#transaction-hide-completed-vorgaenge"
                        )
                    ).to_be_checked()

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='unread_mails']").click()
                    expect(page.locator("#mail-tab")).to_have_class(
                        re.compile("is-active")
                    )

                    page.locator("#dashboard-tab").click()
                    page.locator(
                        "[data-overview-key='upcoming_termine']"
                    ).press("Enter")
                    expect(page.locator("#termine-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator("#termin-hide-completed")
                    ).to_be_checked()
                    expect(
                        page.locator("#termin-special-filter")
                    ).to_be_hidden()

                    page.locator("#dashboard-tab").click()
                    with page.expect_response(
                        lambda response: "/api/termine?" in response.url
                        and "unassigned_upcoming=true" in response.url
                    ):
                        page.locator(
                            "[data-overview-key='unassigned_termine']"
                        ).click()
                    expect(page.locator("#termine-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator("#termin-hide-completed")
                    ).to_be_checked()
                    expect(
                        page.locator("#termin-special-filter")
                    ).to_contain_text(
                        "Nicht zugewiesene anstehende Termine"
                    )

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='unread_mails']").click()
                    expect(page.locator("#mail-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    with page.expect_response(
                        lambda response: "/api/termine?" in response.url
                        and "unassigned_upcoming=false" in response.url
                    ):
                        page.locator("#termine-tab").click()
                    expect(page.locator("#termine-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    expect(
                        page.locator("#termin-special-filter")
                    ).to_be_hidden()

                    page.locator("#dashboard-tab").click()
                    with page.expect_response(
                        lambda response: "/api/termine?" in response.url
                        and "unassigned_upcoming=true" in response.url
                    ):
                        page.locator(
                            "[data-overview-key='unassigned_termine']"
                        ).click()
                    expect(
                        page.locator("#termin-special-filter")
                    ).to_contain_text(
                        "Nicht zugewiesene anstehende Termine"
                    )

                    with page.expect_response(
                        lambda response: "/api/termine?" in response.url
                        and "unassigned_upcoming=false" in response.url
                    ):
                        page.locator(
                            "#termin-special-filter-reset"
                        ).click()
                    expect(
                        page.locator("#termin-special-filter")
                    ).to_be_hidden()

                    page.locator("#dashboard-tab").click()
                    page.locator(
                        "[data-overview-key='unassigned_documents']"
                    ).press(" ")
                    expect(page.locator("#vorgaenge-tab")).to_have_class(
                        re.compile("is-active")
                    )

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='unread_mails']").click()
                    page.evaluate(
                        """
                        () => {
                            const button = document.createElement("button");
                            button.type = "button";
                            button.dataset.overviewKey = "custom_documents";
                            button.dataset.overviewEntity = "documents";
                            button.textContent = "Dokumente";
                            document.querySelector("#overview-cards").append(button);
                        }
                        """
                    )
                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='custom_documents']").click()
                    expect(page.locator("#vorgaenge-tab")).to_have_class(
                        re.compile("is-active")
                    )

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='unread_mails']").click()
                    expect(page.locator("#mail-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    page.evaluate(
                        """
                        () => {
                            const cards = document.querySelector("#overview-cards");
                            for (const [key, entity, label] of [
                                ["__proto__", "todos", "Proto"],
                                ["constructor", "unknown_entity", "Constructor"],
                            ]) {
                                const button = document.createElement("button");
                                button.type = "button";
                                button.dataset.overviewKey = key;
                                button.dataset.overviewEntity = entity;
                                button.textContent = label;
                                cards.append(button);
                            }
                        }
                        """
                    )
                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='__proto__']").click()
                    expect(page.locator("#todo-tab")).to_have_class(
                        re.compile("is-active")
                    )

                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='unread_mails']").click()
                    page.locator("#dashboard-tab").click()
                    page.locator("[data-overview-key='constructor']").click()
                    expect(page.locator("#vorgaenge-tab")).to_have_class(
                        re.compile("is-active")
                    )
                    page.reload(wait_until="networkidle")
                    expect(page.locator("#vorgaenge-tab")).to_have_attribute(
                        "aria-selected", "true"
                    )
                    expect(page.locator("#dashboard-panel")).to_be_hidden()
                    self.assertEqual([], page_errors)
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

    def test_suggestions_are_not_checked_only_because_of_score(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            server = create_server(database_path, port=0)
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page.goto(base_url, wait_until="networkidle")

                    result = page.evaluate(
                        """
                        () => {
                          const form = document.createElement("form");
                          const section = createSuggestionSection(
                            "Transaktionen",
                            "transaction_ids",
                            ["tx-linked"],
                            [
                              {
                                id: "tx-linked",
                                label: "Bestehende Verknuepfung",
                                score: 0.1,
                              },
                              {
                                id: "tx-high-score",
                                label: "Hoher Vorschlag",
                                score: 0.95,
                                source: "suggestion",
                              },
                              {
                                id: "tx-selected",
                                label: "Markierte Verknuepfung",
                                score: 0.2,
                                selected: true,
                              },
                            ],
                          );
                          form.append(section);
                          document.body.append(form);
                          return {
                            checkedById: Object.fromEntries(
                              [...section.querySelectorAll("input[type='checkbox']")]
                                .map((checkbox) => [checkbox.value, checkbox.checked]),
                            ),
                            payload: readSuggestionFields(form),
                          };
                        }
                        """
                    )
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

        self.assertTrue(result["checkedById"]["tx-linked"])
        self.assertTrue(result["checkedById"]["tx-selected"])
        self.assertFalse(result["checkedById"]["tx-high-score"])
        self.assertEqual(
            ["tx-linked", "tx-selected"],
            sorted(result["payload"]["transaction_ids"]),
        )

    def test_mail_vorgang_import_actions_follow_completion_state(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            server = create_server(database_path, port=0)
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page.goto(base_url, wait_until="networkidle")

                    result = page.evaluate(
                        """
                        () => {
                          const section = renderMailVorgangReview(
                            {id: "mail-1", attachments: []},
                            {
                              vorgang: {
                                title: "Mail-Vorgang",
                                description: "",
                                vorgangstyp: "sonstiges",
                              },
                              documents: [],
                              todos: [],
                              termine: [],
                            },
                            {suggestions: {}, candidates: {}},
                            "mail-1",
                            {transactions: []},
                          );
                          document.querySelector("#mail-detail").append(section);
                          const form = section.querySelector(
                            "[data-mail-vorgang-review]"
                          );
                          const checkbox = form.elements.vorgang_completed;
                          const labelsBefore = [
                            ...form.querySelectorAll(
                              "[data-mail-vorgang-import-submit]"
                            ),
                          ].map((button) => button.textContent);
                          checkbox.checked = true;
                          checkbox.dispatchEvent(
                            new Event("input", {bubbles: true})
                          );
                          const labelsAfter = [
                            ...form.querySelectorAll(
                              "[data-mail-vorgang-import-submit]"
                            ),
                          ].map((button) => button.textContent);
                          return {
                            actionBars: form.querySelectorAll(
                              ".mail-vorgang-import-actions"
                            ).length,
                            labelsBefore,
                            labelsAfter,
                            completed: readMailVorgangReviewForm(
                              form
                            ).vorgang.completed,
                            legacyLabel: form.textContent.includes(
                              "Bestätigt importieren"
                            ),
                          };
                        }
                        """
                    )
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

        self.assertEqual(2, result["actionBars"])
        self.assertEqual(
            ["Vorgang anlegen", "Vorgang anlegen"],
            result["labelsBefore"],
        )
        self.assertEqual(
            ["Vorgang abschließen", "Vorgang abschließen"],
            result["labelsAfter"],
        )
        self.assertTrue(result["completed"])
        self.assertFalse(result["legacyLabel"])

    def test_todo_can_be_managed_in_browser(self):
        try:
            from playwright.sync_api import expect, sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            server = create_server(database_path, port=0)
            thread = threading.Thread(
                target=server.serve_forever,
                daemon=True,
            )
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with sync_playwright() as playwright:
                    try:
                        browser = playwright.chromium.launch(headless=True)
                    except Exception as exc:
                        self.skipTest(
                            f"Chromium ist nicht installiert: {exc}"
                        )
                    page = browser.new_page(
                        viewport={"width": 1500, "height": 1000}
                    )
                    page.goto(base_url, wait_until="networkidle")
                    page.locator("#todo-tab").click()
                    page.locator("#todo-form").wait_for()
                    page.locator("#todo-title").fill("Beleg prüfen")
                    page.locator("#todo-description").fill(
                        "Rechnung mit der Transaktion abgleichen."
                    )
                    page.locator("#todo-due-date").fill("2026-06-30")
                    page.locator("#todo-priority").select_option("hoch")
                    page.locator("#todo-vorgaenge").select_option(
                        ["vorgang_tx_newer"]
                    )
                    page.locator("#todo-submit").click()

                    card = page.locator(".todo-card").filter(
                        has_text="Beleg prüfen"
                    )
                    card.wait_for()
                    expect(card).to_contain_text("Neuer Verein")
                    expect(card).to_contain_text("Hohe Priorität")

                    card.locator("[data-toggle-todo]").check()
                    expect(card).to_have_class(re.compile("is-completed"))

                    card.locator("[data-edit-todo]").click()
                    page.locator("#todo-title").fill("Beleg final prüfen")
                    page.locator("#todo-submit").click()
                    card = page.locator(".todo-card").filter(
                        has_text="Beleg final prüfen"
                    )
                    card.wait_for()

                    page.on("dialog", lambda dialog: dialog.accept())
                    card.locator("[data-delete-todo]").click()
                    expect(page.locator(".todo-card")).to_have_count(0)
                    expect(page.locator("#todo-empty")).to_be_visible()
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
