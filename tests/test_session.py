import logging
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from banking_readonly.credentials import Credentials
from banking_readonly.session import (
    _authenticated_url,
    _is_logged_out,
    attempt_automatic_login,
    logout_session,
)


class SessionTests(unittest.TestCase):
    def test_unexpected_login_page_falls_back_to_manual_login(self):
        with (
            patch(
                "banking_readonly.session.submit_credentials",
                side_effect=RuntimeError("unexpected page"),
            ),
            patch("builtins.print") as print_mock,
        ):
            result = attempt_automatic_login(
                Mock(),
                Mock(),
                Credentials(username="user", password="password"),
                logging.getLogger("test"),
            )

        self.assertFalse(result)
        print_mock.assert_called_once()

    def test_expected_login_page_submits_credentials(self):
        with (
            patch("banking_readonly.session.submit_credentials") as submit_mock,
            patch("builtins.print"),
        ):
            result = attempt_automatic_login(
                Mock(),
                Mock(),
                Credentials(username="user", password="password"),
                logging.getLogger("test"),
            )

        self.assertTrue(result)
        submit_mock.assert_called_once()

    def test_recognizes_authenticated_bank_paths(self):
        self.assertTrue(
            _authenticated_url(
                "https://www.sparkasse-gm.de/de/home/onlinebanking/finanzuebersicht.html",
                "sparkasse",
            )
        )
        self.assertTrue(
            _authenticated_url(
                "https://www.vb-oberberg.de/services_cloud/portal/m/banking_start",
                "volksbank",
            )
        )
        self.assertFalse(
            _authenticated_url(
                "https://www.vb-oberberg.de/services_cloud/portal/logout",
                "volksbank",
            )
        )

    def test_recognizes_verified_logout_pages(self):
        sparkasse_page = Mock()
        sparkasse_page.url = (
            "https://www.sparkasse-gm.de/de/home/misc/logout.html"
        )
        sparkasse_page.locator.return_value.inner_text.return_value = (
            "Sie haben sich abgemeldet."
        )
        volksbank_page = Mock()
        volksbank_page.url = (
            "https://www.vb-oberberg.de/services_cloud/portal/logout"
        )
        volksbank_page.locator.return_value.inner_text.return_value = (
            "Sie wurden erfolgreich abgemeldet"
        )

        self.assertTrue(_is_logged_out(sparkasse_page, "sparkasse"))
        self.assertTrue(_is_logged_out(volksbank_page, "volksbank"))

    def test_logout_clicks_action_and_waits_for_confirmation(self):
        page = Mock()
        page.url = (
            "https://www.sparkasse-gm.de/de/home/onlinebanking/finanzuebersicht.html"
        )
        page.is_closed.return_value = False
        context = Mock()
        context.pages = [page]
        action = Mock()
        config = SimpleNamespace(provider="sparkasse", detection=Mock())

        with (
            patch(
                "banking_readonly.session.success_criterion",
                return_value="Text-Muster",
            ),
            patch("banking_readonly.session._logout_action", return_value=action),
            patch("banking_readonly.session._is_logged_out", return_value=True),
        ):
            result = logout_session(
                context,
                config,
                logging.getLogger("test"),
                preferred_page=page,
                timeout_seconds=1,
            )

        self.assertTrue(result)
        action.click.assert_called_once_with()

    def test_missing_logout_action_requests_manual_logout(self):
        page = Mock()
        page.url = (
            "https://www.sparkasse-gm.de/de/home/onlinebanking/finanzuebersicht.html"
        )
        page.is_closed.return_value = False
        context = Mock()
        context.pages = [page]
        config = SimpleNamespace(provider="sparkasse", detection=Mock())

        with (
            patch(
                "banking_readonly.session.success_criterion",
                return_value="Text-Muster",
            ),
            patch("banking_readonly.session._logout_action", return_value=None),
            patch("banking_readonly.session._is_logged_out", return_value=True),
            patch("builtins.print") as print_mock,
        ):
            result = logout_session(
                context,
                config,
                logging.getLogger("test"),
                preferred_page=page,
                timeout_seconds=1,
            )

        self.assertTrue(result)
        print_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
