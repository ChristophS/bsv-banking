from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from banking_dashboard import create_server
from banking_dashboard.mail_integration import (
    DashboardMailManager,
    InboxMailStore,
    MailIntegrationError,
    MailAttachmentContent,
    MicrosoftGraphMailBackend,
    MicrosoftGraphOAuthClient,
    OpenAISpamScorer,
    _mail_category,
    _oauth_error_detail,
    _prepare_and_send_reply,
    _strip_html,
    _updated_outlook_categories,
    fallback_mail_summary,
    fallback_spam_score,
)
from tests.test_dashboard import create_dashboard_database


class FakeSpamScorer:
    model = "test-model"

    def __init__(self):
        self.calls = 0

    def score(self, message):
        self.calls += 1
        return {
            "probability": 0.91,
            "reasons": ["Testbewertung"],
            "source": "test",
        }


class SequenceSpamScorer:
    model = "test-model"

    def __init__(self, probabilities):
        self.probabilities = iter(probabilities)
        self.calls = 0

    def score(self, message):
        self.calls += 1
        return {
            "probability": next(self.probabilities),
            "reasons": ["Sequenzbewertung"],
            "source": "test",
        }


class FakeMailSummarizer:
    model = "test-summary-model"

    def __init__(self):
        self.calls = 0
        self.messages = []

    def summarize(self, message):
        self.calls += 1
        self.messages.append(message)
        return {
            "title": "Testmail zusammengefasst",
            "summary": "Die Mail enthält drei klar zugeordnete Aufgaben.",
            "importantPoints": ["Antwort bis Freitag"],
            "attachments": ["test.txt enthält Hinweise"],
            "actionItems": [
                {
                    "person": "Christoph Süßmeier",
                    "task": "Zahlung prüfen",
                    "due": "Freitag",
                },
                {
                    "person": "Christof Fries",
                    "task": "Termin bestätigen",
                    "due": "",
                },
                {
                    "person": "Christopher Pethe",
                    "task": "Unterlagen senden",
                    "due": "",
                },
            ],
            "source": "test",
            "model": self.model,
        }


class FakeMailBackend:
    def __init__(self):
        self.deleted = []
        self.tags = []
        self.read = []
        self.replies = []
        self.messages = [
            {
                "id": "mail-1",
                "subject": "Testmail",
                "from": {
                    "emailAddress": {
                        "name": "Max Mustermann",
                        "address": "max@example.org",
                    }
                },
                "receivedDateTime": "2026-06-15T10:00:00",
                "bodyPreview": "Bitte dringend verifizieren",
                "folderName": "Junk-E-Mail",
                "category": "Privat",
                "attachmentCount": 1,
                "conversationId": "conversation-1",
            }
        ]

    def list_messages(self):
        return [dict(message) for message in self.messages]

    def list_conversation_messages(self, conversation_id):
        return [
            self.read_message(str(message["id"]))
            for message in self.messages
            if str(message.get("conversationId") or "") == conversation_id
        ]

    def read_message(self, entry_id):
        overview = next(
            (
                message
                for message in self.messages
                if str(message.get("id") or "") == entry_id
            ),
            None,
        )
        if overview is None:
            raise LookupError("Mail wurde nicht gefunden.")
        return {
            "id": entry_id,
            "subject": str(overview.get("subject") or "Testmail"),
            "fromName": (
                overview.get("from", {})
                .get("emailAddress", {})
                .get("name", "Max Mustermann")
            ),
            "fromAddress": (
                overview.get("from", {})
                .get("emailAddress", {})
                .get("address", "max@example.org")
            ),
            "recipients": ["bsv@bsv-bielstein.de"],
            "receivedDateTime": "2026-06-15T10:00:00",
            "body": str(
                overview.get("body")
                or (
                    "Vollstaendiger Mailtext"
                    if entry_id == "mail-1"
                    else f"Vollstaendiger Mailtext {entry_id}"
                )
            ),
            "bodyPreview": str(overview.get("bodyPreview") or ""),
            "folderName": str(overview.get("folderName") or "Posteingang"),
            "category": str(overview.get("category") or "Privat"),
            "conversationId": str(overview.get("conversationId") or ""),
            "attachments": [
                {
                    "attachmentIndex": 1,
                    "filename": "test.txt",
                    "contentType": "text/plain",
                    "size": 12,
                    "text": "Anhangstext",
                }
            ],
        }

    def read_attachment(self, entry_id, attachment_index):
        if entry_id != "mail-1" or attachment_index != 1:
            raise LookupError("Anhang wurde nicht gefunden.")
        return MailAttachmentContent(
            content=b"Anhangstext",
            content_type="text/plain",
            filename="test.txt",
        )

    def set_category(self, entry_id, category):
        self.tags.append((entry_id, category))

    def mark_read(self, entry_id):
        self.read.append(entry_id)

    def delete_message(self, entry_id):
        self.deleted.append(entry_id)

    def send_reply(self, entry_id, body):
        self.replies.append((entry_id, body))


class PagedFakeMailBackend(FakeMailBackend):
    def list_messages_page(self, cursor="", limit=10):
        start = int(cursor or 0)
        end = min(start + int(limit or 10), len(self.messages))
        return {
            "messages": [dict(message) for message in self.messages[start:end]],
            "next_cursor": str(end) if end < len(self.messages) else "",
        }


class MailIntegrationUnitTests(unittest.TestCase):
    def test_explicit_category_overrides_address_classification(self):
        self.assertEqual(
            "Privat",
            _mail_category(
                ["vorstand@bsv-bielstein.de"],
                "Projekt, Privat",
            ),
        )
        self.assertEqual(
            "BSV",
            _mail_category(["private@example.org"], "BSV"),
        )

    def test_category_change_preserves_unrelated_outlook_categories(self):
        self.assertEqual(
            "Projekt, Privat",
            _updated_outlook_categories(
                "Projekt, BSV",
                "Privat",
                separator=",",
            ),
        )

    def test_reply_preserves_history_and_escapes_html(self):
        reply = Mock()
        reply.HTMLBody = "<div>Original</div>"
        item = Mock()
        item.Reply.return_value = reply

        _prepare_and_send_reply(item, "<Danke>\nZeile 2")

        self.assertIn("&lt;Danke&gt;<br>Zeile 2", reply.HTMLBody)
        self.assertTrue(reply.HTMLBody.endswith("<div>Original</div>"))
        reply.Send.assert_called_once_with()

    def test_html_mail_body_omits_css_comments_and_invisible_padding(self):
        body = """
        <html>
          <head>
            <style><!--
              body {margin:0 auto!important; padding:0}
              table {border-spacing:0}
            --></style>
          </head>
          <body>
            <!--
              .links-black {color:#1a1a1a!important}
            -->
            <div>Letzte Chance Ihren Promo-Code zu nutzen</div>
            <div>\u200c\u200b\u200d\u200e\u200f\ufeff</div>
            <p>Hallo Christoph,</p>
          </body>
        </html>
        """

        text = _strip_html(body)

        self.assertIn("Letzte Chance Ihren Promo-Code zu nutzen", text)
        self.assertIn("Hallo Christoph,", text)
        self.assertNotIn("margin:0", text)
        self.assertNotIn("links-black", text)
        self.assertNotIn("<!--", text)
        self.assertNotIn("\u200b", text)

    def test_junk_folder_receives_high_local_spam_score(self):
        result = fallback_spam_score(
            {
                "subject": "Test",
                "folderName": "Junk-E-Mail",
                "from": {"emailAddress": {"address": "x@example.org"}},
                "bodyPreview": "",
            }
        )

        self.assertEqual(0.95, result["probability"])
        self.assertEqual("local_fallback", result["source"])

    def test_openai_spam_score_is_used_for_mail_list(self):
        scorer = OpenAISpamScorer("api-key", "gpt-test")
        scorer.score = Mock(
            return_value={
                "probability": 0.73,
                "reasons": ["Remotebewertung"],
                "source": "openai",
            }
        )
        manager = DashboardMailManager(FakeMailBackend(), scorer)

        payload = manager.list_messages()

        scorer.score.assert_called_once()
        self.assertEqual(0.73, payload["messages"][0]["spamProbability"])
        self.assertEqual("openai", payload["messages"][0]["spamSource"])

    def test_manager_allows_explicit_delete_independent_of_threshold(self):
        backend = FakeMailBackend()
        manager = DashboardMailManager(backend, FakeSpamScorer())
        payload = manager.list_messages()

        self.assertEqual(0.91, payload["messages"][0]["spamProbability"])
        manager.update_settings({"spam_threshold": 0.95})

        result = manager.delete("mail-1")

        self.assertTrue(result["deleted"])
        self.assertEqual(["mail-1"], backend.deleted)

    def test_processed_spam_score_is_reused_after_restart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "mail.sqlite3"
            backend = FakeMailBackend()
            scorer = FakeSpamScorer()

            first_manager = DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            )
            first_manager.list_messages()
            second_manager = DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            )
            payload = second_manager.list_messages()

        self.assertEqual(1, scorer.calls)
        self.assertEqual(0.91, payload["messages"][0]["spamProbability"])

    def test_changed_mail_is_scored_again(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "mail.sqlite3"
            backend = FakeMailBackend()
            scorer = FakeSpamScorer()
            DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()
            backend.messages[0]["bodyPreview"] = "Geaenderter Inhalt"

            DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()

        self.assertEqual(2, scorer.calls)

    def test_archived_zero_percent_score_is_scored_again(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "mail.sqlite3"
            backend = FakeMailBackend()
            scorer = SequenceSpamScorer([0.0, 0.42])

            DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()
            payload = DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()

        self.assertEqual(2, scorer.calls)
        self.assertEqual(0.42, payload["messages"][0]["spamProbability"])

    def test_small_score_is_reused_in_memory_for_consistent_loads(self):
        backend = FakeMailBackend()
        scorer = SequenceSpamScorer([0.0049, 0.35])
        manager = DashboardMailManager(backend, scorer)

        first_payload = manager.list_messages()
        payload = manager.list_messages()

        self.assertEqual(1, scorer.calls)
        self.assertEqual(0.0049, first_payload["messages"][0]["spamProbability"])
        self.assertEqual(0.0049, payload["messages"][0]["spamProbability"])

    def test_small_scores_below_reuse_threshold_are_scored_after_restart(self):
        for probability in (0.0, 0.001, 0.0049):
            with self.subTest(probability=probability):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    cache_path = Path(temporary_directory) / "mail.sqlite3"
                    backend = FakeMailBackend()
                    scorer = SequenceSpamScorer([probability, 0.42])

                    DashboardMailManager(
                        backend,
                        scorer,
                        cache_path=cache_path,
                    ).list_messages()
                    payload = DashboardMailManager(
                        backend,
                        scorer,
                        cache_path=cache_path,
                    ).list_messages()

                self.assertEqual(2, scorer.calls)
                self.assertEqual(0.42, payload["messages"][0]["spamProbability"])

    def test_score_at_reuse_threshold_is_reused_after_restart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "mail.sqlite3"
            backend = FakeMailBackend()
            scorer = SequenceSpamScorer([0.005, 0.42])

            DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()
            payload = DashboardMailManager(
                backend,
                scorer,
                cache_path=cache_path,
            ).list_messages()

        self.assertEqual(1, scorer.calls)
        self.assertEqual(0.005, payload["messages"][0]["spamProbability"])

    def test_summary_distinguishes_similar_board_member_names(self):
        manager = DashboardMailManager(
            FakeMailBackend(),
            FakeSpamScorer(),
            summarizer=FakeMailSummarizer(),
        )

        result = manager.summarize("mail-1")
        action_items = result["summary"]["actionItems"]

        self.assertTrue(action_items[0]["isForChristoph"])
        self.assertEqual("christoph", action_items[0]["assignmentStatus"])
        self.assertFalse(action_items[1]["isForChristoph"])
        self.assertEqual("other", action_items[1]["assignmentStatus"])
        self.assertFalse(action_items[2]["isForChristoph"])
        self.assertEqual("other", action_items[2]["assignmentStatus"])

    def test_fallback_summary_detects_missing_invoice_request(self):
        summary = fallback_mail_summary(
            {
                "subject": "Belege",
                "body": (
                    "Hier noch die Belege.\n\n"
                    "Hier muss nichts mehr ueberwiesen werden, ausser "
                    "Ueberberg.\n\n"
                    "Diese Rechnung liegt mir aber nicht vor.\n\n"
                    "Bitte einmal an mich, damit ich die mit ablegen kann."
                ),
            }
        )

        action_items = summary["actionItems"]

        self.assertTrue(action_items)
        self.assertIn("rechnung von ueberberg", action_items[0]["task"].casefold())
        self.assertEqual("Christoph Suessmeier", action_items[0]["person"])

    def test_quick_summary_uses_local_mail_without_summarizer_call(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            summarizer = FakeMailSummarizer()
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                summarizer=summarizer,
                inbox_database_path=database_path,
            )
            inbox_id = manager.list_messages()["messages"][0]["id"]

            result = manager.summarize_quick(inbox_id)

        self.assertTrue(result["quick"])
        self.assertEqual("local_fallback", result["summary"]["source"])
        self.assertEqual(0, summarizer.calls)

    def test_processed_summary_is_reused_after_restart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "mail.sqlite3"
            backend = FakeMailBackend()
            summarizer = FakeMailSummarizer()
            first_manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                cache_path=cache_path,
                summarizer=summarizer,
            )
            first_result = first_manager.summarize("mail-1")
            second_manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                cache_path=cache_path,
                summarizer=summarizer,
            )
            second_result = second_manager.summarize("mail-1")

        self.assertFalse(first_result["cached"])
        self.assertTrue(second_result["cached"])
        self.assertEqual(1, summarizer.calls)

    def test_inbox_id_is_stable_and_full_mail_is_persisted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            first_manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            first_id = first_manager.list_messages()["messages"][0]["id"]
            connection = sqlite3.connect(database_path)
            try:
                listed_message = connection.execute(
                    """
                    SELECT body
                    FROM inbox_messages
                    WHERE inbox_id = ?
                    """,
                    (first_id,),
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual("", listed_message[0])
            first_manager.read_message(first_id)
            second_manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            second_id = second_manager.list_messages()["messages"][0]["id"]
            offline_manager = DashboardMailManager(
                None,
                FakeSpamScorer(),
                summarizer=FakeMailSummarizer(),
                inbox_database_path=database_path,
            )
            offline_detail = offline_manager.read_message(first_id)

            connection = sqlite3.connect(database_path)
            try:
                message = connection.execute(
                    """
                    SELECT source_message_id, body
                    FROM inbox_messages
                    WHERE inbox_id = ?
                    """,
                    (first_id,),
                ).fetchone()
                attachment = connection.execute(
                    """
                    SELECT filename, extracted_text, content
                    FROM inbox_attachments
                    WHERE inbox_id = ?
                    """,
                    (first_id,),
                ).fetchone()
            finally:
                connection.close()

            online_attachment = first_manager.read_attachment(first_id, 1)
            offline_attachment = offline_manager.read_attachment(first_id, 1)

        self.assertTrue(first_id.startswith("inbox_"))
        self.assertEqual(first_id, second_id)
        self.assertEqual(("mail-1", "Vollstaendiger Mailtext"), message)
        self.assertEqual("test.txt", attachment[0])
        self.assertEqual("Anhangstext", attachment[1])
        self.assertEqual(b"Anhangstext", bytes(attachment[2]))
        self.assertEqual(
            "Vollstaendiger Mailtext",
            offline_detail["message"]["body"],
        )

        self.assertEqual(b"Anhangstext", online_attachment.content)
        self.assertEqual(b"Anhangstext", offline_attachment.content)

    def test_internet_message_id_survives_changed_outlook_entry_id(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            backend.messages[0]["internetMessageId"] = "<mail@example.org>"
            first_id = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            ).list_messages()["messages"][0]["id"]
            backend.messages[0]["id"] = "mail-moved"
            second_id = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            ).list_messages()["messages"][0]["id"]

        self.assertEqual(first_id, second_id)

    def test_paged_mail_loading_keeps_previous_pages_actionable(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = PagedFakeMailBackend()
            backend.messages.append(
                {
                    **backend.messages[0],
                    "id": "mail-2",
                    "subject": "Zweite Mail",
                    "conversationId": "conversation-2",
                }
            )
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            first_page = manager.list_messages(limit=1)
            second_page = manager.list_messages(
                cursor=first_page["next_cursor"],
                limit=1,
            )
            first_id = first_page["messages"][0]["id"]
            second_id = second_page["messages"][0]["id"]

            result = manager.delete_selected(
                {"entry_ids": [first_id, second_id]}
            )

        self.assertEqual(2, result["deleted_count"])
        self.assertCountEqual(["mail-1", "mail-2"], backend.deleted)

    def test_explicit_delete_removes_local_mail_record(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            inbox_id = manager.list_messages()["messages"][0]["id"]
            manager.read_message(inbox_id)

            manager.delete(inbox_id)

            connection = sqlite3.connect(database_path)
            try:
                message_count = connection.execute(
                    "SELECT COUNT(*) FROM inbox_messages WHERE inbox_id = ?",
                    (inbox_id,),
                ).fetchone()[0]
                attachment_count = connection.execute(
                    "SELECT COUNT(*) FROM inbox_attachments WHERE inbox_id = ?",
                    (inbox_id,),
                ).fetchone()[0]
            finally:
                connection.close()

        self.assertEqual(0, message_count)
        self.assertEqual(0, attachment_count)

    def test_full_target_mail_load_marks_stale_local_unread_as_read(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            inbox_store = InboxMailStore(database_path)
            stale_id = inbox_store.upsert_overview(
                {
                    "source": "graph",
                    "id": "stale-target",
                    "subject": "Schon gelesen",
                    "receivedDateTime": "2026-06-14T10:00:00",
                    "bodyPreview": "Alt",
                    "folderName": "Posteingang",
                    "isRead": False,
                }
            )
            archive_id = inbox_store.upsert_overview(
                {
                    "source": "graph",
                    "id": "archive-unread",
                    "subject": "Archiv",
                    "receivedDateTime": "2026-06-13T10:00:00",
                    "bodyPreview": "Archiv",
                    "folderName": "Archiv",
                    "isRead": False,
                }
            )
            backend = FakeMailBackend()
            backend.messages = [
                {
                    **backend.messages[0],
                    "id": "current-target",
                    "subject": "Aktuell ungelesen",
                    "folderName": "Posteingang",
                    "conversationId": "current-conversation",
                }
            ]
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )

            current_id = manager.list_messages()["messages"][0]["id"]

            connection = sqlite3.connect(database_path)
            try:
                rows = dict(
                    connection.execute(
                        """
                        SELECT inbox_id, is_read
                        FROM inbox_messages
                        WHERE inbox_id IN (?, ?, ?)
                        """,
                        (stale_id, archive_id, current_id),
                    ).fetchall()
                )
            finally:
                connection.close()

        self.assertEqual(1, rows[stale_id])
        self.assertEqual(0, rows[archive_id])
        self.assertEqual(0, rows[current_id])

    def test_cached_mail_list_uses_local_unread_without_backend(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            inbox_store = InboxMailStore(database_path)
            current_id = inbox_store.upsert_overview(
                {
                    "source": "graph",
                    "id": "cached-current",
                    "subject": "Lokal ungelesen",
                    "receivedDateTime": "2026-06-20T10:00:00",
                    "bodyPreview": "Sofort sichtbar",
                    "folderName": "BSV",
                    "isRead": False,
                }
            )
            inbox_store.upsert_overview(
                {
                    "source": "graph",
                    "id": "cached-read",
                    "subject": "Schon gelesen",
                    "receivedDateTime": "2026-06-20T09:00:00",
                    "bodyPreview": "Nicht anzeigen",
                    "folderName": "BSV",
                    "isRead": True,
                }
            )
            inbox_store.upsert_overview(
                {
                    "source": "graph",
                    "id": "cached-archive",
                    "subject": "Archiv",
                    "receivedDateTime": "2026-06-20T08:00:00",
                    "bodyPreview": "Nicht anzeigen",
                    "folderName": "Archiv",
                    "isRead": False,
                }
            )
            manager = DashboardMailManager(
                None,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )

            payload = manager.cached_messages()

        self.assertTrue(payload["local"])
        self.assertFalse(payload["available"])
        self.assertEqual([current_id], [mail["id"] for mail in payload["messages"]])

    def test_conversation_actions_apply_to_whole_thread(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            backend.messages.append(
                {
                    **backend.messages[0],
                    "id": "mail-2",
                    "subject": "Re: Testmail",
                    "body": "Antwort aus dem Verlauf",
                    "bodyPreview": "Antwort aus dem Verlauf",
                    "folderName": "Posteingang",
                    "conversationId": "conversation-1",
                }
            )
            summarizer = FakeMailSummarizer()
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                summarizer=summarizer,
                inbox_database_path=database_path,
            )
            inbox_id = manager.list_messages()["messages"][0]["id"]

            summary = manager.summarize(inbox_id)
            delete_result = manager.delete(inbox_id)

        self.assertTrue(summary["conversation"]["isConversation"])
        self.assertEqual(2, summary["conversation"]["messageCount"])
        self.assertIn("Antwort aus dem Verlauf", summarizer.messages[0]["body"])
        self.assertEqual(2, delete_result["affected_count"])
        self.assertCountEqual(["mail-1", "mail-2"], backend.deleted)

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            backend.messages.append(
                {
                    **backend.messages[0],
                    "id": "mail-2",
                    "subject": "Re: Testmail",
                    "body": "Antwort aus dem Verlauf",
                    "bodyPreview": "Antwort aus dem Verlauf",
                    "folderName": "Posteingang",
                    "conversationId": "conversation-1",
                }
            )
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            inbox_id = manager.list_messages()["messages"][0]["id"]
            tag_result = manager.toggle_tag(inbox_id, {"tag": "BSV"})
            read_result = manager.mark_read(inbox_id)

        self.assertEqual(2, tag_result["affected_count"])
        self.assertCountEqual(
            [("mail-1", "BSV"), ("mail-2", "BSV")],
            backend.tags,
        )
        self.assertEqual(2, read_result["affected_count"])
        self.assertCountEqual(["mail-1", "mail-2"], backend.read)

    def test_single_mail_actions_do_not_load_remote_conversation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            backend.list_conversation_messages = Mock(
                side_effect=AssertionError(
                    "Einzelaktionen duerfen keine Conversation-Suche starten."
                )
            )
            manager = DashboardMailManager(
                backend,
                FakeSpamScorer(),
                inbox_database_path=database_path,
            )
            inbox_id = manager.list_messages()["messages"][0]["id"]

            read_result = manager.mark_read(inbox_id)

        self.assertEqual(1, read_result["affected_count"])
        self.assertEqual(["mail-1"], backend.read)
        backend.list_conversation_messages.assert_not_called()

    def test_graph_oauth_device_code_is_reported_without_blocking(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache_path = Path(temporary_directory) / "token.json"
            client = MicrosoftGraphOAuthClient(
                "client-id",
                "https://login.example.test/tenant",
                cache_path=cache_path,
            )
            client._post_form = Mock(
                return_value={
                    "device_code": "device-code",
                    "user_code": "ABCD-EFGH",
                    "verification_uri": "https://microsoft.com/devicelogin",
                    "expires_in": 900,
                    "interval": 0,
                }
            )

            with patch("builtins.print"):
                with self.assertRaises(MailIntegrationError) as raised:
                    client.access_token()

            self.assertIn("ABCD-EFGH", str(raised.exception))
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "device-code",
                cached["device_flow"]["device_code"],
            )

            client._post_form = Mock(
                return_value={
                    "access_token": "access-token",
                    "refresh_token": "refresh-token",
                    "expires_in": 3600,
                }
            )

            self.assertEqual("access-token", client.access_token())

    def test_graph_lists_unread_messages_from_target_folders(self):
        backend = MicrosoftGraphMailBackend(Mock())
        messages_by_folder = {
            "inbox": [
                {
                    "id": "graph-inbox",
                    "subject": "Aus Posteingang",
                    "receivedDateTime": "2026-06-20T09:00:00+00:00",
                }
            ],
            "folder-bsv": [
                {
                    "id": "graph-bsv",
                    "subject": "Aus BSV",
                    "receivedDateTime": "2026-06-20T10:00:00+00:00",
                }
            ],
            "junkemail": [
                {
                    "id": "graph-junk",
                    "subject": "Aus Junk",
                    "receivedDateTime": "2026-06-19T10:00:00+00:00",
                }
            ],
        }

        def request_json(method, path, **kwargs):
            if path.startswith("/me/mailFolders?"):
                return {
                    "value": [
                        {"id": "folder-bsv", "displayName": "BSV"},
                        {"id": "folder-archive", "displayName": "Archiv"},
                    ]
                }
            if "/childFolders?" in path:
                return {"value": []}
            if "/messages?" in path:
                folder_id = path.split("/me/mailFolders/", 1)[1].split(
                    "/messages?",
                    1,
                )[0]
                self.assertNotEqual("folder-archive", folder_id)
                values = []
                for message in messages_by_folder.get(folder_id, []):
                    values.append(
                        {
                            "from": {
                                "emailAddress": {
                                    "name": "Max",
                                    "address": "max@example.org",
                                }
                            },
                            "toRecipients": [],
                            "ccRecipients": [],
                            "bccRecipients": [],
                            "bodyPreview": "Bitte pruefen",
                            "parentFolderId": folder_id,
                            "categories": ["BSV"],
                            "hasAttachments": False,
                            "internetMessageId": (
                                f"<{message['id']}@example.org>"
                            ),
                            "conversationId": "graph-conversation",
                            "isRead": False,
                            **message,
                        }
                    )
                return {"value": values}
            raise AssertionError(f"Unexpected request path: {path}")

        backend._request_json = Mock(side_effect=request_json)

        messages = backend.list_messages()

        self.assertEqual(
            ["graph-bsv", "graph-inbox", "graph-junk"],
            [message["id"] for message in messages],
        )
        self.assertEqual("BSV", messages[0]["folderName"])
        requested_paths = [
            call_args[0][1] for call_args in backend._request_json.call_args_list
        ]
        self.assertFalse(
            any(path.startswith("/me/messages?") for path in requested_paths)
        )
        folder_message_paths = [
            path for path in requested_paths if "/messages?" in path
        ]
        self.assertEqual(3, len(folder_message_paths))
        self.assertTrue(folder_message_paths[0].startswith("/me/mailFolders/inbox/"))
        for request_path in folder_message_paths:
            query = parse_qs(urlparse(request_path).query)
            self.assertEqual(
                [
                    "receivedDateTime ge 1900-01-01T00:00:00Z "
                    "and isRead eq false"
                ],
                query["$filter"],
            )

    def test_graph_message_page_returns_first_target_folder_page_immediately(self):
        backend = MicrosoftGraphMailBackend(Mock())

        def request_json(method, path, **kwargs):
            if path.startswith("/me/mailFolders?"):
                self.fail("Ordner-Discovery darf vor der ersten Seite nicht laufen.")
            if "/messages?" in path:
                folder_id = path.split("/me/mailFolders/", 1)[1].split(
                    "/messages?",
                    1,
                )[0]
                if folder_id == "inbox":
                    return {
                        "value": [
                            {
                                "id": "graph-inbox",
                                "subject": "Aus Posteingang",
                                "from": {"emailAddress": {}},
                                "receivedDateTime": "2026-06-20T10:00:00+00:00",
                                "parentFolderId": folder_id,
                                "isRead": False,
                            }
                        ]
                    }
                self.fail("Weitere Ordner duerfen fuer die erste Seite nicht gelesen werden.")
            raise AssertionError(f"Unexpected request path: {path}")

        backend._request_json = Mock(side_effect=request_json)

        page = backend.list_messages_page(limit=10)

        self.assertEqual(["graph-inbox"], [message["id"] for message in page["messages"]])
        self.assertTrue(page["next_cursor"])
        folder_message_paths = [
            call_args[0][1]
            for call_args in backend._request_json.call_args_list
            if "/messages?" in call_args[0][1]
        ]
        self.assertEqual(1, len(folder_message_paths))

    def test_graph_message_page_rejects_non_graph_cursor(self):
        backend = MicrosoftGraphMailBackend(Mock())
        backend._request_json = Mock()

        with self.assertRaisesRegex(ValueError, "Mail-Listen-Cursor"):
            backend.list_messages_page("legacy-cursor")

        backend._request_json.assert_not_called()

    def test_graph_reads_content_bytes_from_file_attachment_type(self):
        backend = MicrosoftGraphMailBackend(Mock())

        def request_json(method, path, **kwargs):
            if path.startswith("/me/messages/graph-mail/attachments?"):
                return {
                    "value": [
                        {
                            "id": "graph-attachment",
                            "name": "rechnung.pdf",
                            "contentType": "application/pdf",
                            "size": 5,
                        }
                    ]
                }
            if path.startswith(
                "/me/messages/graph-mail/attachments/"
                "graph-attachment/microsoft.graph.fileAttachment?"
            ):
                query = parse_qs(urlparse(path).query)
                self.assertIn("contentBytes", query["$select"][0])
                return {
                    "id": "graph-attachment",
                    "name": "rechnung.pdf",
                    "contentType": "application/pdf",
                    "size": 5,
                    "contentBytes": "SGFsbG8=",
                }
            raise AssertionError(f"Unexpected request path: {path}")

        backend._request_json = Mock(side_effect=request_json)

        attachment = backend.read_attachment("graph-mail", 1)

        self.assertEqual(b"Hallo", attachment.content)
        self.assertEqual("application/pdf", attachment.content_type)
        requested_paths = [
            call_args[0][1] for call_args in backend._request_json.call_args_list
        ]
        self.assertTrue(
            any(
                "/microsoft.graph.fileAttachment?" in path
                for path in requested_paths
            )
        )

    def test_oauth_invalid_client_error_keeps_actionable_description(self):
        detail = _oauth_error_detail(
            {
                "error": "invalid_client",
                "error_description": (
                    "AADSTS700016: Application was not found."
                ),
            },
            "https://login.microsoftonline.com/consumers",
        )

        self.assertIn("AADSTS700016", detail)
        self.assertIn("Application (client) ID", detail)
        self.assertIn("/consumers", detail)


class MailIntegrationHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        database_path = (
            Path(self.temporary_directory.name) / "transactions.sqlite3"
        )
        create_dashboard_database(database_path)
        self.backend = FakeMailBackend()
        self.server = create_server(
            database_path,
            port=0,
            mail_backend=self.backend,
            mail_spam_scorer=FakeSpamScorer(),
            mail_summarizer=FakeMailSummarizer(),
        )
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

    def test_mail_read_tag_reply_attachment_and_delete_flow(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            listed = json.load(response)
        self.assertEqual(1, listed["count"])
        self.assertEqual(0.91, listed["messages"][0]["spamProbability"])
        inbox_id = listed["messages"][0]["id"]
        self.assertTrue(inbox_id.startswith("inbox_"))

        with urlopen(
            self.base_url + f"/api/mail/{inbox_id}",
            timeout=5,
        ) as response:
            detail = json.load(response)
        self.assertEqual(
            "Vollstaendiger Mailtext",
            detail["message"]["body"],
        )
        self.assertEqual(
            listed["messages"][0]["spamProbability"],
            detail["spam"]["probability"],
        )

        quick_summary_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/summary?quick=1",
            method="POST",
        )
        with urlopen(quick_summary_request, timeout=5) as response:
            quick_summary = json.load(response)
        self.assertTrue(quick_summary["quick"])
        self.assertEqual(
            "local_fallback",
            quick_summary["summary"]["source"],
        )

        summary_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/summary",
            method="POST",
        )
        with urlopen(summary_request, timeout=5) as response:
            summary = json.load(response)
        self.assertEqual(
            "Die Mail enthält drei klar zugeordnete Aufgaben.",
            summary["summary"]["summary"],
        )
        self.assertTrue(
            summary["summary"]["actionItems"][0]["isForChristoph"]
        )

        with urlopen(
            self.base_url + f"/api/mail/{inbox_id}/attachments/1",
            timeout=5,
        ) as response:
            self.assertEqual(b"Anhangstext", response.read())
            self.assertEqual("text/plain", response.headers.get_content_type())

        tag_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/tag",
            data=json.dumps({"tag": "BSV"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(tag_request, timeout=5) as response:
            self.assertEqual("BSV", json.load(response)["tag"])
        self.assertEqual([("mail-1", "BSV")], self.backend.tags)

        reply_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/reply",
            data=json.dumps({"body": "Danke."}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(reply_request, timeout=5) as response:
            self.assertTrue(json.load(response)["sent"])
        self.assertEqual([("mail-1", "Danke.")], self.backend.replies)

        threshold_request = Request(
            self.base_url + "/api/mail/settings",
            data=json.dumps({"spam_threshold": 0.92}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(threshold_request, timeout=5):
            pass
        delete_request = Request(
            self.base_url + f"/api/mail/{inbox_id}",
            method="DELETE",
        )
        with urlopen(delete_request, timeout=5) as response:
            self.assertTrue(json.load(response)["deleted"])
        self.assertEqual(["mail-1"], self.backend.deleted)

    def test_mail_can_be_marked_read_without_loading_detail(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]
        read_request = Request(
            self.base_url + f"/api/mail/{inbox_id}/read",
            method="POST",
        )

        with urlopen(read_request, timeout=5) as response:
            payload = json.load(response)

        self.assertTrue(payload["marked_read"])
        self.assertEqual(["mail-1"], self.backend.read)

    def test_selected_mails_can_be_deleted_without_spam_threshold(self):
        with urlopen(self.base_url + "/api/mail", timeout=5) as response:
            inbox_id = json.load(response)["messages"][0]["id"]
        threshold_request = Request(
            self.base_url + "/api/mail/settings",
            data=json.dumps({"spam_threshold": 0.99}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="PATCH",
        )
        with urlopen(threshold_request, timeout=5):
            pass
        delete_request = Request(
            self.base_url + "/api/mail/delete-selected",
            data=json.dumps({"entry_ids": [inbox_id]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(delete_request, timeout=5) as response:
            payload = json.load(response)

        self.assertEqual(1, payload["deleted_count"])
        self.assertEqual(["mail-1"], self.backend.deleted)

    def test_mail_can_be_linked_to_vorgang(self):
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
            linked = json.load(response)
        self.assertEqual([vorgangs_id], linked["vorgangs_ids"])
        self.assertEqual(vorgangs_id, linked["vorgaenge"][0]["vorgangs_id"])
        self.assertIn("titel", linked["vorgaenge"][0])
        self.assertIn("status", linked["vorgaenge"][0])

        with urlopen(link_request, timeout=5) as response:
            linked_again = json.load(response)
        self.assertEqual([vorgangs_id], linked_again["vorgangs_ids"])
        self.assertEqual(1, len(linked_again["vorgaenge"]))

        with urlopen(
            self.base_url + f"/api/mail/{inbox_id}/vorgaenge",
            timeout=5,
        ) as response:
            payload = json.load(response)
        self.assertEqual([vorgangs_id], payload["vorgangs_ids"])
        self.assertEqual(vorgangs_id, payload["vorgaenge"][0]["vorgangs_id"])

        unlink_request = Request(
            self.base_url
            + f"/api/mail/{inbox_id}/vorgaenge/{vorgangs_id}",
            method="DELETE",
        )
        with urlopen(unlink_request, timeout=5) as response:
            payload = json.load(response)
        self.assertEqual([], payload["vorgangs_ids"])
        self.assertEqual([], payload["vorgaenge"])


class MailIntegrationBrowserTests(unittest.TestCase):
    def test_mail_workspace_reads_tags_zooms_and_replies(self):
        try:
            from playwright.sync_api import expect, sync_playwright
        except ImportError:
            self.skipTest("Playwright ist nicht installiert.")

        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "transactions.sqlite3"
            create_dashboard_database(database_path)
            backend = FakeMailBackend()
            backend.messages.append(
                {
                    **backend.messages[0],
                    "id": "mail-2",
                    "subject": "Zweite Testmail",
                    "bodyPreview": "Normale zweite Nachricht",
                    "folderName": "Posteingang",
                    "conversationId": "conversation-2",
                }
            )
            server = create_server(
                database_path,
                port=0,
                mail_backend=backend,
                mail_spam_scorer=FakeSpamScorer(),
                mail_summarizer=FakeMailSummarizer(),
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
                    page = browser.new_page(viewport={"width": 1500, "height": 1000})
                    page.goto(base_url, wait_until="networkidle")
                    page.locator("#mail-tab").click()
                    page.locator(".mail-list-item").first.wait_for()
                    mail_one_id = page.locator(
                        ".mail-list-item",
                    ).filter(has_text="Testmail").first.get_attribute(
                        "data-mail-id"
                    )
                    mail_two_id = page.locator(
                        ".mail-list-item",
                    ).filter(has_text="Zweite Testmail").get_attribute(
                        "data-mail-id"
                    )
                    self.assertTrue(mail_one_id.startswith("inbox_"))
                    self.assertTrue(mail_two_id.startswith("inbox_"))
                    expect(
                        page.locator("#mail-detail")
                    ).to_contain_text("Mail auswählen")
                    page.locator(
                        f"[data-summarize-mail='{mail_one_id}']"
                    ).click()
                    page.locator(".mail-summary-panel").wait_for()
                    expect(
                        page.locator(".mail-summary-panel")
                    ).to_contain_text("ToDos für Christoph Süßmeier")
                    expect(
                        page.locator(".mail-summary-panel")
                    ).to_contain_text("Zahlung prüfen")
                    expect(
                        page.locator("#mail-detail")
                    ).to_contain_text("Mail auswählen")
                    page.locator(
                        f"[data-open-mail='{mail_one_id}']"
                    ).click()
                    page.locator(".mail-body-text").wait_for()

                    self.assertIn(
                        "Vollstaendiger Mailtext",
                        page.locator(".mail-body-text").inner_text(),
                    )
                    self.assertIn(
                        "Anhangstext",
                        page.locator(".mail-attachment-text").inner_text(),
                    )
                    expect(
                        page.locator("#mail-detail [data-summarize-mail]")
                    ).to_be_visible()
                    expect(
                        page.locator("#mail-detail [data-mark-mail-read]")
                    ).to_be_visible()
                    expect(
                        page.locator(".mail-delete-button")
                    ).to_be_enabled()
                    link_form = page.locator("[data-link-mail-vorgang]")
                    expect(link_form).to_be_visible()
                    expect(
                        page.locator(".mail-vorgang-empty")
                    ).to_contain_text("Noch keinem Vorgang zugeordnet")
                    candidate_count = page.locator(
                        ".mail-vorgang-candidate"
                    ).count()
                    self.assertGreater(candidate_count, 0)
                    link_form.locator("input[name='vorgangs_id']").first.check()
                    link_form.locator("button[type='submit']").click()
                    expect(
                        page.locator(".mail-vorgang-item")
                    ).to_have_count(1)
                    expect(
                        page.locator(".mail-vorgang-item")
                    ).to_contain_text("Entfernen")
                    expect(
                        page.locator(".mail-vorgang-candidate")
                    ).to_have_count(candidate_count - 1)
                    page.locator(
                        ".mail-vorgang-item [data-unlink-mail-vorgang]"
                    ).click()
                    expect(
                        page.locator(".mail-vorgang-empty")
                    ).to_contain_text("Noch keinem Vorgang zugeordnet")
                    bulk_delete = page.locator("#mail-delete-spam")
                    expect(bulk_delete).to_be_enabled()
                    expect(bulk_delete).to_have_text("2 Spam-Mails löschen")

                    zoom = page.locator("[data-mail-zoom-range]")
                    zoom.fill("200")
                    zoom.dispatch_event("input")
                    self.assertEqual(
                        "200%",
                        page.locator(
                            "[data-mail-preview-content]"
                        ).evaluate("(node) => node.style.width"),
                    )

                    detail_tag = page.locator(
                        ".mail-detail-actions [data-toggle-mail-tag]"
                    )
                    detail_tag.click()
                    expect(detail_tag).to_have_text("BSV")
                    self.assertEqual([("mail-1", "BSV")], backend.tags)

                    page.locator("#mail-spam-threshold").fill("95")
                    page.locator("#mail-spam-threshold").dispatch_event(
                        "change"
                    )
                    expect(
                        page.locator(".mail-delete-button")
                    ).to_be_enabled()
                    expect(bulk_delete).to_be_disabled()

                    page.locator(".mail-reply-form textarea").fill("Danke.")
                    page.locator(".mail-reply-form button[type='submit']").click()
                    page.get_by_text(
                        "Antwort wurde gesendet."
                    ).wait_for()
                    self.assertEqual([("mail-1", "Danke.")], backend.replies)

                    page.locator(
                        f"#mail-detail [data-mark-mail-read='{mail_one_id}']"
                    ).click()
                    expect(
                        page.locator(f"[data-mail-id='{mail_one_id}']")
                    ).to_have_count(0)
                    self.assertEqual(["mail-1"], backend.read)

                    delete_checkbox = page.locator(
                        f"[data-select-mail-delete='{mail_two_id}']"
                    )
                    delete_checkbox.check()
                    selected_delete = page.locator("#mail-delete-selected")
                    expect(selected_delete).to_be_enabled()
                    expect(selected_delete).to_have_text(
                        "1 markierte Mail löschen"
                    )
                    selected_delete.click()
                    expect(page.locator(".mail-list-item")).to_have_count(0)
                    page.get_by_text("1 markierte Mail gelöscht").wait_for()
                    self.assertEqual(["mail-2"], backend.deleted)
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
