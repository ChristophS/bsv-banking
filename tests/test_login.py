import unittest
from unittest.mock import Mock

from banking_readonly.config import (
    AppConfig,
    CredentialsConfig,
    DetectionConfig,
    ExportConfig,
    RuntimeConfig,
)
from banking_readonly.credentials import Credentials
from banking_readonly.login import LoginFormError, submit_credentials


def app_config() -> AppConfig:
    return AppConfig(
        login_url="https://bank.test/auth/login?client=banking",
        credentials=CredentialsConfig(
            mode="env",
            env_file=None,
            username_variable="USER",
            password_variable="PASSWORD",
            username_selector="#username",
            password_selector="#password",
            submit_selector="button[type='submit']",
        ),
        export=ExportConfig(
            output_dir=Mock(),
            format="CSV",
            period="FROM_SEARCH",
            download_timeout_seconds=60,
        ),
        detection=DetectionConfig(
            success_selector=None,
            success_url_pattern=r"^https://bank\.test/portal",
            timeout_seconds=60,
            poll_interval_seconds=0.5,
            stable_seconds=1.0,
        ),
        runtime=RuntimeConfig(
            profile_dir=Mock(),
            log_dir=Mock(),
            screenshot_dir=Mock(),
            navigation_timeout_seconds=30,
        ),
    )


def sparkasse_config() -> AppConfig:
    base = app_config()
    return AppConfig(
        login_url="https://www.sparkasse-gm.de/de/home.html",
        credentials=CredentialsConfig(
            mode="env",
            env_file=None,
            username_variable="SPARKASSE_USERNAME",
            password_variable="SPARKASSE_PASSWORD",
            username_selector="input[autocomplete='username']:visible",
            password_selector="input[type='password']:visible",
            submit_selector="input[type='submit'][title='Anmelden']:visible",
            username_submit_selector=(
                "input[type='submit'][title='Weiter']:visible"
            ),
        ),
        export=base.export,
        detection=base.detection,
        runtime=base.runtime,
        provider="sparkasse",
    )


def locator_collection(element=None, count=1):
    locator = Mock()
    locator.count.return_value = count
    locator.filter.return_value = locator
    locator.first = element if element is not None else locator
    return locator


class LoginTests(unittest.TestCase):
    def test_fills_only_configured_fields_and_submits(self):
        username = Mock()
        password = Mock()
        submit = Mock()
        for locator in (username, password, submit):
            locator.first = locator

        page = Mock()
        page.url = "https://bank.test/auth/login"
        page.locator.side_effect = {
            "#username": username,
            "#password": password,
            "button[type='submit']": submit,
        }.get

        submit_credentials(
            page,
            app_config(),
            Credentials(username="test-user", password="test-password"),
        )

        username.fill.assert_called_once_with("test-user")
        password.fill.assert_called_once_with("test-password")
        submit.click.assert_called_once_with()

    def test_rejects_different_page_before_touching_dom(self):
        page = Mock()
        page.url = "https://bank.test/portal"

        with self.assertRaisesRegex(LoginFormError, "nicht auf"):
            submit_credentials(
                page,
                app_config(),
                Credentials(username="test-user", password="test-password"),
            )

        page.locator.assert_not_called()

    def test_sparkasse_fills_username_then_pin_and_submits(self):
        username = Mock()
        username.is_visible.return_value = True
        username_submit = Mock()
        password = Mock()
        submit = Mock()

        username_locator = locator_collection(username)
        username_submit_locator = locator_collection(username_submit)
        password_locator = locator_collection(password)
        submit_locator = locator_collection(submit)
        cookie_locator = locator_collection(count=0)

        form = Mock()
        form.count.return_value = 1
        form.locator.return_value = submit_locator
        password.locator.return_value = form

        selectors = sparkasse_config().credentials
        page = Mock()
        page.url = "https://www.sparkasse-gm.de/de/home.html"
        page.locator.side_effect = {
            ".if6_outer.if6_eprivacy a[title='Ablehnen']": cookie_locator,
            selectors.username_selector: username_locator,
            selectors.username_submit_selector: username_submit_locator,
            selectors.password_selector: password_locator,
        }.get

        submit_credentials(
            page,
            sparkasse_config(),
            Credentials(username="spark-user", password="spark-pin"),
        )

        username.wait_for.assert_called_once_with(state="visible", timeout=10_000)
        username.fill.assert_called_once_with("spark-user")
        username_submit.click.assert_called_once_with()
        password.wait_for.assert_called_once_with(state="visible", timeout=10_000)
        password.fill.assert_called_once_with("spark-pin")
        submit.click.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
