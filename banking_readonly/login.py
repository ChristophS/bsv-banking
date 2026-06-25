from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from .config import AppConfig
from .credentials import Credentials


class LoginFormError(RuntimeError):
    """Raised when credentials cannot be submitted on the configured login page."""


def submit_credentials(
    page: Any,
    config: AppConfig,
    credentials: Credentials,
) -> None:
    credential_config = config.credentials
    if credential_config.mode != "env":
        raise LoginFormError("Automatischer Login ist nicht konfiguriert.")

    if config.provider == "sparkasse":
        _submit_sparkasse_credentials(page, config, credentials)
        return

    _submit_volksbank_credentials(page, config, credentials)


def _submit_volksbank_credentials(
    page: Any,
    config: AppConfig,
    credentials: Credentials,
) -> None:
    _assert_login_page(page.url, config.login_url)
    credential_config = config.credentials
    username = page.locator(credential_config.username_selector).first
    password = page.locator(credential_config.password_selector).first
    submit = page.locator(credential_config.submit_selector).first

    username.wait_for(state="visible", timeout=10_000)
    password.wait_for(state="visible", timeout=10_000)
    submit.wait_for(state="visible", timeout=10_000)

    username.fill(credentials.username)
    password.fill(credentials.password)
    submit.click()


def _submit_sparkasse_credentials(
    page: Any,
    config: AppConfig,
    credentials: Credentials,
) -> None:
    _assert_same_page(page.url, config.login_url)
    credential_config = config.credentials
    _dismiss_sparkasse_cookies(page)

    username = page.locator(credential_config.username_selector)
    if username.count() == 0 or not username.first.is_visible():
        login_button = page.get_by_role(
            "button",
            name="Anmelden - Melden Sie sich an",
            exact=True,
        )
        if login_button.count() != 1:
            raise LoginFormError(
                "Sparkassen-Anmeldeschaltflaeche wurde nicht eindeutig gefunden."
            )
        login_button.click()

    page.locator(credential_config.username_selector).first.wait_for(
        state="visible", timeout=10_000
    )
    username = _single_visible(
        page.locator(credential_config.username_selector),
        "Sparkassen-Feld 'Anmeldename'",
    )
    username_submit = _single_visible(
        page.locator(credential_config.username_submit_selector),
        "Sparkassen-Schaltflaeche 'Weiter'",
    )
    username.fill(credentials.username)
    username_submit.click()

    password_locator = page.locator(credential_config.password_selector)
    password_locator.first.wait_for(state="visible", timeout=10_000)
    password = _single_visible(
        password_locator,
        "Sparkassen-Feld 'Online-Banking-PIN'",
    )
    password.fill(credentials.password)

    form = password.locator("xpath=ancestor::form[1]")
    submit_scope = form if form.count() == 1 else page
    submit = _single_visible(
        submit_scope.locator(credential_config.submit_selector),
        "Sparkassen-Schaltflaeche 'Anmelden'",
    )
    submit.click()


def _dismiss_sparkasse_cookies(page: Any) -> None:
    reject = page.locator(
        ".if6_outer.if6_eprivacy a[title='Ablehnen']"
    )
    if reject.count() == 1 and reject.is_visible():
        reject.click()


def _single_visible(locator: Any, description: str) -> Any:
    visible = locator.filter(visible=True)
    if visible.count() != 1:
        raise LoginFormError(
            f"{description} wurde {visible.count()}-mal statt genau einmal gefunden."
        )
    return visible.first


def _assert_login_page(current_url: str, configured_url: str) -> None:
    current = urlsplit(current_url)
    configured = urlsplit(configured_url)
    current_scope = (current.scheme.lower(), current.hostname, current.port, current.path)
    configured_scope = (
        configured.scheme.lower(),
        configured.hostname,
        configured.port,
        configured.path,
    )
    if current_scope != configured_scope:
        raise LoginFormError(
            "Credential-Eingabe abgebrochen: Browser befindet sich nicht auf "
            "der exakt konfigurierten Loginseite."
        )


def _assert_same_page(current_url: str, configured_url: str) -> None:
    current = urlsplit(current_url)
    configured = urlsplit(configured_url)
    current_scope = (
        current.scheme.lower(),
        current.hostname,
        current.port,
        current.path.rstrip("/"),
    )
    configured_scope = (
        configured.scheme.lower(),
        configured.hostname,
        configured.port,
        configured.path.rstrip("/"),
    )
    if current_scope != configured_scope:
        raise LoginFormError(
            "Credential-Eingabe abgebrochen: Browser befindet sich nicht auf "
            "der konfigurierten Sparkassen-Startseite."
        )
