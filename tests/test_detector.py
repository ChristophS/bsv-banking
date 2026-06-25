import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from banking_readonly.detector import _text_matches, url_matches
from banking_readonly.logging_setup import SensitiveDataFilter
from banking_readonly.runner import _save_error_screenshot


class DetectorTests(unittest.TestCase):
    def test_url_pattern_matches_dashboard(self):
        pattern = r"^https://bank\.test/(overview|accounts)"
        self.assertTrue(url_matches(pattern, "https://bank.test/overview"))
        self.assertFalse(url_matches(pattern, "https://bank.test/login"))

    def test_text_pattern_matches_formatted_iban(self):
        page = Mock()
        page.locator.return_value.inner_text.return_value = (
            "Konto Veranstaltungen DE29 3845 0000 0000 3592 32"
        )

        self.assertTrue(
            _text_matches(
                page,
                r"DE29\s*3845\s*0000\s*0000\s*3592\s*32",
            )
        )

    def test_text_pattern_tolerates_navigation_timeout(self):
        page = Mock()
        page.locator.return_value.inner_text.side_effect = TimeoutError()

        self.assertFalse(_text_matches(page, "Konto"))

    def test_log_filter_removes_url_query_and_userinfo(self):
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="Fehler bei https://user:secret@bank.test/login?token=abc",
            args=(),
            exc_info=None,
        )

        SensitiveDataFilter().filter(record)

        self.assertEqual(
            record.getMessage(),
            "Fehler bei https://bank.test/login?<redacted>",
        )

    def test_error_screenshot_is_written(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            page = Mock()
            page.is_closed.return_value = False

            def write_screenshot(path, full_page, mask, mask_color):
                self.assertFalse(full_page)
                self.assertEqual(mask_color, "#000000")
                self.assertGreaterEqual(len(mask), 1)
                Path(path).write_bytes(b"fake-png")

            page.screenshot.side_effect = write_screenshot
            context = Mock()
            context.pages = [page]

            result = _save_error_screenshot(
                context, Path(temp_dir), logging.getLogger("test")
            )

            self.assertIsNotNone(result)
            self.assertTrue(result.is_file())
            self.assertEqual(result.read_bytes(), b"fake-png")


if __name__ == "__main__":
    unittest.main()
