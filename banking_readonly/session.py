from __future__ import annotations

import logging
import re
import time
from typing import Any, Optional
from urllib.parse import urlsplit

from .config import AppConfig
from .credentials import Credentials
from .detector import success_criterion
from .login import submit_credentials


class LogoutError(RuntimeError):
    """Raised when an authenticated session cannot be logged out."""


def open_fresh_page(context: Any) -> Any:
    page = context.new_page()
    for existing in list(context.pages):
        if existing is page or existing.is_closed():
            continue
        try:
            existing.close()
        except Exception:
            pass
    return page


def attempt_automatic_login(
    page: Any,
    config: AppConfig,
    credentials: Credentials,
    logger: logging.Logger,
) -> bool:
    try:
        submit_credentials(page, config, credentials)
    except Exception as exc:
        logger.warning(
            "Automatischer Login nicht moeglich (%s). "
            "Manueller Login wird abgewartet.",
            type(exc).__name__,
        )
        print(
            "\nDie erwartete Loginmaske wurde nicht eindeutig erkannt. "
            "Bitte Login und eine gegebenenfalls erforderliche MFA jetzt "
            "manuell im Browser abschliessen.\n"
        )
        return False

    logger.info("Lokale Zugangsdaten wurden einmalig abgesendet.")
    print(
        "\nZugangsdaten wurden lokal eingesetzt. Bitte unerwartete Hinweise "
        "oder eine gegebenenfalls angeforderte MFA manuell bearbeiten.\n"
    )
    return True


def logout_session(
    context: Any,
    config: AppConfig,
    logger: logging.Logger,
    preferred_page: Optional[Any] = None,
    timeout_seconds: int = 120,
) -> bool:
    page = _authenticated_page(context, config, preferred_page)
    if page is None:
        logger.info("Keine aktive Onlinebanking-Sitzung zum Abmelden erkannt.")
        return False

    automatic_logout = False
    try:
        action = _logout_action(page, config.provider)
        if action is not None:
            action.click()
            automatic_logout = True
    except Exception as exc:
        logger.warning(
            "Automatische Abmeldung nicht moeglich (%s).",
            type(exc).__name__,
        )

    if not automatic_logout:
        print(
            "\nDie Abmeldeschaltflaeche wurde nicht eindeutig erkannt. "
            "Bitte jetzt im Browser manuell abmelden.\n"
        )

    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        pages = [candidate for candidate in context.pages if not candidate.is_closed()]
        if not pages:
            raise LogoutError(
                "Browser wurde geschlossen, bevor die Abmeldung bestaetigt war."
            )
        if any(_is_logged_out(candidate, config.provider) for candidate in pages):
            logger.info(
                "Onlinebanking-Sitzung bei %s erfolgreich abgemeldet.",
                config.provider,
            )
            return True
        time.sleep(0.25)

    raise LogoutError(
        f"Abmeldung bei {config.provider} wurde innerhalb von "
        f"{timeout_seconds} Sekunden nicht bestaetigt."
    )


def _authenticated_page(
    context: Any,
    config: AppConfig,
    preferred_page: Optional[Any],
) -> Optional[Any]:
    candidates = []
    if preferred_page is not None:
        candidates.append(preferred_page)
    candidates.extend(
        page for page in reversed(context.pages) if page is not preferred_page
    )
    for page in candidates:
        if page is None or page.is_closed():
            continue
        if success_criterion(page, config.detection) or _authenticated_url(
            page.url, config.provider
        ):
            return page
    return None


def _authenticated_url(url: str, provider: str) -> bool:
    path = urlsplit(url).path
    if provider == "sparkasse":
        return path.startswith("/de/home/onlinebanking/")
    return (
        path.startswith("/services_cloud/portal/")
        and not path.startswith("/services_cloud/portal/logout")
    )


def _logout_action(page: Any, provider: str) -> Optional[Any]:
    if provider == "sparkasse":
        actions = page.locator("button").filter(
            has_text=re.compile(r"^\s*Abmelden\s*$")
        ).filter(visible=True)
    else:
        actions = page.locator(
            "button[data-automation-id='logout-button']"
        ).filter(visible=True)
    return actions.first if actions.count() == 1 else None


def _is_logged_out(page: Any, provider: str) -> bool:
    try:
        path = urlsplit(page.url).path
        body = page.locator("body").inner_text(timeout=500)
    except Exception:
        return False

    if provider == "sparkasse":
        return (
            path == "/de/home/misc/logout.html"
            or "Sie haben sich abgemeldet." in body
        )
    return (
        path.startswith("/services_cloud/portal/logout")
        or "Sie wurden erfolgreich abgemeldet" in body
    )
