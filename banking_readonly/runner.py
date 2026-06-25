from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .config import AppConfig
from .credentials import load_credentials
from .detector import DetectionResult, wait_for_success
from .security import ensure_private_directory, protect_file
from .session import attempt_automatic_login, logout_session, open_fresh_page


class DependencyError(RuntimeError):
    """Raised when Playwright or its Chromium browser is unavailable."""


def run_login_test(config: AppConfig, logger: logging.Logger) -> DetectionResult:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise DependencyError(
            "Playwright fehlt. Installation siehe README: "
            "'python -m pip install -r requirements.txt'."
        ) from exc

    credentials = None
    if config.credentials.mode == "env":
        credentials = load_credentials(config.credentials)

    ensure_private_directory(config.runtime.profile_dir)
    ensure_private_directory(config.runtime.screenshot_dir)
    logger.info("Starte sichtbaren Chromium-Browser im rein lesenden Testmodus.")
    with sync_playwright() as playwright:
        context: Optional[Any] = None
        page: Optional[Any] = None
        logout_attempted = False
        try:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(config.runtime.profile_dir),
                headless=False,
                accept_downloads=False,
                viewport=None,
            )
            page = open_fresh_page(context)
            page.goto(
                config.login_url,
                wait_until="domcontentloaded",
                timeout=config.runtime.navigation_timeout_seconds * 1000,
            )

            if config.credentials.mode == "env":
                if credentials is None:
                    raise RuntimeError("Credentials wurden nicht vorgeladen.")
                try:
                    attempt_automatic_login(page, config, credentials, logger)
                finally:
                    del credentials
                    credentials = None
            else:
                logger.info(
                    "Loginseite geladen. Zugangsdaten und MFA ausschliesslich "
                    "manuell im Browser eingeben."
                )
                print(
                    "\nBitte Login und MFA jetzt manuell im Chromium-Fenster "
                    "durchfuehren.\n"
                    "Das Programm beobachtet nur URL und DOM und fuehrt keine "
                    "Banking-Aktion aus.\n"
                )

            result = wait_for_success(context, config.detection)
            page = result.page or page
            logger.info("Login erfolgreich erkannt durch %s.", result.criterion)
            logout_attempted = True
            logout_session(context, config, logger, preferred_page=page)
            return result
        except Exception:
            screenshot_path = _save_error_screenshot(
                context,
                config.runtime.screenshot_dir,
                logger,
                sensitive_selectors=_sensitive_selectors(config),
            )
            if screenshot_path:
                logger.error("Fehler-Screenshot gespeichert: %s", screenshot_path)
            if context is not None and not logout_attempted:
                try:
                    logout_session(
                        context,
                        config,
                        logger,
                        preferred_page=page,
                    )
                except Exception as logout_exc:
                    logger.warning(
                        "Abmeldung nach Fehler nicht bestaetigt: %s",
                        logout_exc,
                    )
            raise
        finally:
            if credentials is not None:
                del credentials
            if context is not None:
                try:
                    context.close()
                except Exception as exc:
                    logger.warning("Browserkontext konnte nicht sauber schliessen: %s", exc)


def _save_error_screenshot(
    context: Optional[Any],
    screenshot_dir: Path,
    logger: logging.Logger,
    sensitive_selectors: tuple[str, ...] = (),
) -> Optional[Path]:
    if context is None:
        logger.error(
            "Kein Screenshot moeglich, da der Browserkontext nicht gestartet wurde."
        )
        return None

    ensure_private_directory(screenshot_dir)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    screenshot_path = screenshot_dir / f"error_{timestamp}.png"

    for page in reversed(context.pages):
        if page.is_closed():
            continue
        try:
            masks = [page.locator(selector) for selector in sensitive_selectors]
            masks.append(page.locator("input[type='password']"))
            page.screenshot(
                path=str(screenshot_path),
                full_page=False,
                mask=masks,
                mask_color="#000000",
            )
            protect_file(screenshot_path)
            return screenshot_path
        except Exception as exc:
            logger.warning("Screenshot der aktuellen Seite fehlgeschlagen: %s", exc)

    logger.error("Kein Screenshot moeglich, da keine offene Seite vorhanden ist.")
    return None


def _sensitive_selectors(config: AppConfig) -> tuple[str, ...]:
    selectors = (
        config.credentials.username_selector,
        config.credentials.password_selector,
    )
    return tuple(selector for selector in selectors if selector)
