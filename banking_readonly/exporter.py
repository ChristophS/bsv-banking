from __future__ import annotations

import logging
import re
import shutil
import time
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Optional, Sequence
from urllib.parse import urljoin, urlsplit

from .balance_snapshot import (
    AccountBalanceObservation,
    write_balance_snapshot,
)
from .config import AppConfig, ExportAccount
from .credentials import load_credentials
from .detector import wait_for_success
from .runner import DependencyError, _save_error_screenshot, _sensitive_selectors
from .security import ensure_private_directory, protect_file
from .session import attempt_automatic_login, logout_session, open_fresh_page


class ExportError(RuntimeError):
    """Raised when a safe, unambiguous CSV export is not possible."""


AllowedAccount = ExportAccount


ALLOWED_ACCOUNTS = (
    AllowedAccount("Hauptkonto", "DE31384621350101206017", "hauptkonto.csv"),
    AllowedAccount("Rücklagen", "DE09384621350101206025", "ruecklagen.csv"),
    AllowedAccount("Ausstattung", "DE98384621350103038014", "ausstattung.csv"),
    AllowedAccount("Sparkonto", "DE25384621350101206416", "sparkonto.csv"),
)

_GERMAN_MONEY_PATTERN = re.compile(
    r"(?<![\d.,])"
    r"(?P<amount>[+\-\u2212]?(?:\d{1,3}(?:\.\d{3})*|\d+),\d{2})"
    r"\s*(?P<currency>EUR|€)",
    re.IGNORECASE,
)
_LABELED_BALANCE_PATTERN = re.compile(
    r"(?:Kontostand|Saldo)"
    r"[^0-9+\-\u2212]{0,60}"
    + _GERMAN_MONEY_PATTERN.pattern,
    re.IGNORECASE,
)


def run_csv_export(config: AppConfig, logger: logging.Logger) -> tuple[Path, ...]:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise DependencyError(
            "Playwright fehlt. Installation siehe README: "
            "'python -m pip install -r requirements.txt'."
        ) from exc

    if config.provider == "volksbank":
        if config.export.format != "CSV" or config.export.period != "FROM_SEARCH":
            raise ExportError("Nur CSV mit Zeitraum FROM_SEARCH ist zugelassen.")
        accounts = config.export.accounts or ALLOWED_ACCOUNTS
    else:
        if (
            config.export.format != "CSV_MT940"
            or config.export.period != "CURRENT_VIEW"
        ):
            raise ExportError(
                "Fuer die Sparkasse ist nur Excel (CSV-MT940) zugelassen."
            )
        accounts = config.export.accounts
        if not accounts:
            raise ExportError("Keine Sparkassenkonten konfiguriert.")

    credentials = None
    if config.credentials.mode == "env":
        credentials = load_credentials(config.credentials)

    ensure_private_directory(config.runtime.profile_dir)
    ensure_private_directory(config.runtime.screenshot_dir)
    run_dir = _create_run_directory(config.export.output_dir)
    logger.info(
        "Starte sichtbaren Chromium-Browser fuer %d CSV-Exporte bei %s.",
        len(accounts),
        config.provider,
    )

    with sync_playwright() as playwright:
        context: Optional[Any] = None
        page: Optional[Any] = None
        logout_attempted = False
        export_completed = False
        try:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(config.runtime.profile_dir),
                headless=False,
                accept_downloads=True,
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
                    raise ExportError("Credentials wurden nicht vorgeladen.")
                try:
                    attempt_automatic_login(page, config, credentials, logger)
                finally:
                    del credentials
                    credentials = None
            else:
                print(
                    "\nBitte Login und MFA jetzt manuell im Chromium-Fenster "
                    "durchfuehren.\n"
                )

            result = wait_for_success(context, config.detection)
            page = result.page or page
            page.wait_for_timeout(1500)
            _dismiss_optional_cookies(page)

            if config.provider == "sparkasse":
                downloaded = _export_sparkasse_accounts(
                    page, config, accounts, run_dir, logger
                )
            else:
                downloaded = _export_volksbank_accounts(
                    page, config, accounts, run_dir, logger
                )

            logger.info(
                "Alle %d freigegebenen CSV-Exporte abgeschlossen.",
                len(downloaded),
            )
            export_completed = True
            logout_attempted = True
            logout_session(context, config, logger, preferred_page=page)
            return downloaded
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
            if not export_completed:
                _remove_partial_run(run_dir, config.export.output_dir, logger)
            raise
        finally:
            if credentials is not None:
                del credentials
            if context is not None:
                try:
                    context.close()
                except Exception as exc:
                    logger.warning("Browserkontext konnte nicht sauber schliessen: %s", exc)


def _export_volksbank_accounts(
    page: Any,
    config: AppConfig,
    accounts: Sequence[AllowedAccount],
    run_dir: Path,
    logger: logging.Logger,
) -> tuple[Path, ...]:
    balance_observations = {}
    for account in accounts:
        action = _find_account_action(page, account)
        balance, currency = extract_volksbank_account_balance(
            _account_action_text(action),
            account.name,
        )
        balance_observations[account.iban] = AccountBalanceObservation(
            account_name=account.name,
            account_number=account.iban,
            balance=balance,
            currency=currency,
            captured_at=datetime.now().astimezone(),
        )

    action = _find_account_action(page, accounts[0])
    action.click()
    page.wait_for_url(
        re.compile(r"/services_cloud/portal/webcomp/banking/umsaetze"),
        timeout=config.runtime.navigation_timeout_seconds * 1000,
    )
    page.wait_for_timeout(1500)

    downloaded = []
    for account in accounts:
        _select_account(page, page, account)
        page.wait_for_timeout(1500)
        dialog = _open_export_dialog(page)
        _select_radio(dialog, config.export.format)
        _select_radio(dialog, config.export.period)

        export_button = dialog.get_by_role(
            "button", name="Exportieren", exact=True
        )
        destination = run_dir / account.filename
        _download_to(
            page,
            export_button,
            destination,
            account,
            config.export.download_timeout_seconds,
        )
        downloaded.append(destination)
        logger.info(
            "CSV fuer %s (IBAN endet auf %s) gespeichert.",
            account.name,
            account.iban[-4:],
        )
        _close_export_dialog(page)

    write_balance_snapshot(
        run_dir,
        config.provider,
        balance_observations,
    )
    return tuple(downloaded)


def _export_sparkasse_accounts(
    page: Any,
    config: AppConfig,
    accounts: Sequence[AllowedAccount],
    run_dir: Path,
    logger: logging.Logger,
) -> tuple[Path, ...]:
    overview_url = page.url
    configured_host = (urlsplit(config.login_url).hostname or "").lower()
    overview = urlsplit(overview_url)
    bank_domain = configured_host.removeprefix("www.")
    overview_host = (overview.hostname or "").lower()
    if (
        overview.scheme.lower() != "https"
        or not bank_domain
        or (
            overview_host != configured_host
            and overview_host != bank_domain
            and not overview_host.endswith(f".{bank_domain}")
        )
    ):
        raise ExportError(
            "Sparkassen-Kontoübersicht liegt nicht auf der konfigurierten "
            "HTTPS-Bankdomain."
        )

    downloaded = []
    balance_observations = {}
    for index, account in enumerate(accounts):
        if index:
            page.goto(
                overview_url,
                wait_until="domcontentloaded",
                timeout=config.runtime.navigation_timeout_seconds * 1000,
            )
            page.wait_for_timeout(1200)

        balance, currency = _read_sparkasse_account_balance(page, account)
        balance_observations[account.iban] = AccountBalanceObservation(
            account_name=account.name,
            account_number=account.iban,
            balance=balance,
            currency=currency,
            captured_at=datetime.now().astimezone(),
        )
        action = _find_sparkasse_account_action(page, account)
        action.click()
        _wait_for_sparkasse_export_action(
            page, config.runtime.navigation_timeout_seconds
        )

        _open_sparkasse_export_dialog(page)
        export_button = _find_sparkasse_format_download_action(page)

        destination = run_dir / account.filename
        _download_sparkasse_csv(
            page,
            export_button,
            destination,
            account,
            config.export.download_timeout_seconds,
        )
        downloaded.append(destination)
        logger.info(
            "Sparkassen-CSV-MT940 fuer %s (IBAN endet auf %s) gespeichert.",
            account.name,
            account.iban[-4:],
        )

    write_balance_snapshot(
        run_dir,
        config.provider,
        balance_observations,
    )
    return tuple(downloaded)


def _download_to(
    page: Any,
    action: Any,
    destination: Path,
    account: AllowedAccount,
    timeout_seconds: int,
) -> None:
    with page.expect_download(timeout=timeout_seconds * 1000) as download_info:
        action.click()
    download = download_info.value
    failure = download.failure()
    if failure:
        raise ExportError(f"Download fuer {account.name} fehlgeschlagen: {failure}")
    if not download.suggested_filename.lower().endswith(".csv"):
        raise ExportError(f"Download fuer {account.name} ist keine CSV-Datei.")
    download.save_as(str(destination))
    protect_file(destination)
    if not destination.is_file() or destination.stat().st_size <= 0:
        raise ExportError(f"Leere oder fehlende CSV-Datei fuer {account.name}.")


def _download_sparkasse_csv(
    page: Any,
    action: Any,
    destination: Path,
    account: AllowedAccount,
    timeout_seconds: int,
) -> None:
    href = action.get_attribute("href")
    if not href:
        raise ExportError(
            f"Sparkassen-Exportlink fuer {account.name} hat keine Ziel-URL."
        )

    download_url = urljoin(page.url, href)
    page_url = urlsplit(page.url)
    target_url = urlsplit(download_url)
    if (
        target_url.scheme.lower() != "https"
        or target_url.hostname != page_url.hostname
        or target_url.path != page_url.path
    ):
        raise ExportError(
            f"Sparkassen-Exportlink fuer {account.name} verlaesst die "
            "aktuelle HTTPS-Umsatzseite."
        )

    response = page.context.request.get(
        download_url,
        timeout=timeout_seconds * 1000,
    )
    if response.status != 200:
        raise ExportError(
            f"Sparkassen-Export fuer {account.name} lieferte HTTP "
            f"{response.status}."
        )

    content_type = response.headers.get("content-type", "").lower()
    disposition = response.headers.get("content-disposition", "").lower()
    if not content_type.startswith("text/csv"):
        raise ExportError(
            f"Sparkassen-Export fuer {account.name} ist kein CSV-Inhalt."
        )
    if "attachment" not in disposition or ".csv" not in disposition:
        raise ExportError(
            f"Sparkassen-Export fuer {account.name} ist kein CSV-Attachment."
        )

    body = response.body()
    if not body:
        raise ExportError(f"Leere CSV-Antwort fuer {account.name}.")
    try:
        destination.write_bytes(body)
    except OSError as exc:
        raise ExportError(
            f"CSV fuer {account.name} konnte nicht gespeichert werden: {exc}"
        ) from exc
    protect_file(destination)


def normalize_iban(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def unique_matching_index(texts: Sequence[str], account: AllowedAccount) -> int:
    matches = [
        index
        for index, text in enumerate(texts)
        if account.name.casefold() in text.casefold()
        and account.iban in normalize_iban(text)
    ]
    if len(matches) != 1:
        raise ExportError(
            f"{account.name} mit freigegebener IBAN wurde "
            f"{len(matches)}-mal statt genau einmal gefunden."
        )
    return matches[0]


def _find_sparkasse_account_action(page: Any, account: AllowedAccount) -> Any:
    card = _find_sparkasse_account_card(page, account)
    action = card.locator("a.mkp-identifier-link").filter(visible=True)
    if action.count() != 1:
        raise ExportError(
            f"Kontolink fuer Sparkassenkonto {account.name} wurde "
            f"{action.count()}-mal statt genau einmal gefunden."
        )

    displayed_name = _compact_text(action.first.inner_text())
    if displayed_name.casefold() != account.name.casefold():
        raise ExportError(
            f"Kontoname fuer IBAN-Endung {account.iban[-4:]} stimmt nicht "
            f"mit der Allowlist ueberein: '{displayed_name}'."
        )
    return action.first


def _find_sparkasse_account_card(page: Any, account: AllowedAccount) -> Any:
    cards = page.locator(
        f".mkp-card-bank-account[data-iban='{account.iban}']"
    ).filter(visible=True)
    if cards.count() != 1:
        raise ExportError(
            f"Sparkassenkonto {account.name} mit freigegebener IBAN wurde "
            f"{cards.count()}-mal statt genau einmal gefunden."
        )
    return cards.first


def _read_sparkasse_account_balance(
    page: Any,
    account: AllowedAccount,
) -> tuple[Decimal, str]:
    card = _find_sparkasse_account_card(page, account)
    return extract_sparkasse_account_balance(card.inner_text(), account.name)


def extract_sparkasse_account_balance(
    card_text: str,
    account_name: str,
) -> tuple[Decimal, str]:
    text = _compact_text(card_text).replace("\u00a0", " ")
    labeled = _unique_money_matches(_LABELED_BALANCE_PATTERN, text)
    candidates = labeled or _unique_money_matches(_GERMAN_MONEY_PATTERN, text)
    if len(candidates) != 1:
        raise ExportError(
            f"Kontostand fuer Sparkassenkonto {account_name} wurde "
            f"{len(candidates)}-mal statt genau einmal gefunden."
        )
    return candidates[0]


def extract_volksbank_account_balance(
    card_text: str,
    account_name: str,
) -> tuple[Decimal, str]:
    text = _compact_text(card_text).replace("\u00a0", " ")
    labeled = _unique_money_matches(_LABELED_BALANCE_PATTERN, text)
    candidates = labeled or _unique_money_matches(_GERMAN_MONEY_PATTERN, text)
    if len(candidates) != 1:
        raise ExportError(
            f"Kontostand fuer Volksbankkonto {account_name} wurde "
            f"{len(candidates)}-mal statt genau einmal gefunden."
        )
    return candidates[0]


def _unique_money_matches(
    pattern: re.Pattern[str],
    text: str,
) -> list[tuple[Decimal, str]]:
    values = []
    for match in pattern.finditer(text):
        amount_text = match.group("amount").replace("\u2212", "-")
        try:
            amount = Decimal(
                amount_text.replace(".", "").replace(",", ".")
            ).quantize(Decimal("0.01"))
        except InvalidOperation as exc:
            raise ExportError(
                "Sparkassen-Kontostand hat ein ungueltiges Zahlenformat."
            ) from exc
        currency = match.group("currency").upper().replace("€", "EUR")
        value = (amount, currency)
        if value not in values:
            values.append(value)
    return values


def _wait_for_sparkasse_export_action(page: Any, timeout_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if _sparkasse_export_actions(page):
            return
        page.wait_for_timeout(100)
    raise ExportError(
        "Nach dem Kontoaufruf wurde keine Schaltflaeche 'Exportieren' gefunden."
    )


def _open_sparkasse_export_dialog(page: Any) -> None:
    if _sparkasse_format_is_visible(page):
        return

    actions = _sparkasse_export_actions(page)
    if len(actions) != 1:
        raise ExportError(
            "Sparkassen-Schaltflaeche 'Exportieren' wurde "
            f"{len(actions)}-mal statt genau einmal gefunden."
        )
    actions[0].click()

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if _sparkasse_format_is_visible(page):
            return
        page.wait_for_timeout(100)
    raise ExportError(
        "Sparkassen-Exportdialog mit 'Excel (CSV-MT940)' wurde nicht sichtbar."
    )


def _sparkasse_export_actions(page: Any) -> list[Any]:
    buttons = page.get_by_role(
        "button", name="Exportieren", exact=True
    ).filter(visible=True)
    return [buttons.nth(index) for index in range(buttons.count())]


def _sparkasse_format_is_visible(page: Any) -> bool:
    pattern = re.compile(r"^Excel\s*\(CSV-MT940\)$", re.IGNORECASE)
    return page.locator("a", has_text=pattern).filter(visible=True).count() == 1


def _find_sparkasse_format_download_action(page: Any) -> Any:
    pattern = re.compile(r"^Excel\s*\(CSV-MT940\)$", re.IGNORECASE)
    links = page.locator("a", has_text=pattern).filter(visible=True)
    if links.count() != 1:
        raise ExportError(
            "Sparkassen-Downloadlink 'Excel (CSV-MT940)' wurde "
            f"{links.count()}-mal statt genau einmal gefunden."
        )
    return links.first


def _action_name(action: Any) -> str:
    values = (
        action.inner_text(),
        action.get_attribute("value"),
        action.get_attribute("title"),
        action.get_attribute("aria-label"),
    )
    return next((_compact_text(value) for value in values if _compact_text(value)), "")


def _compact_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


def _create_run_directory(output_dir: Path) -> Path:
    ensure_private_directory(output_dir)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    return ensure_private_directory(output_dir / timestamp)


def _dismiss_optional_cookies(page: Any) -> None:
    reject = page.locator("#onetrust-reject-all-handler")
    if reject.is_visible():
        reject.click()
        page.wait_for_timeout(300)


def _find_account_action(page: Any, account: AllowedAccount) -> Any:
    actions = page.locator("button.konto-item-action")
    texts = [_account_action_text(actions.nth(index)) for index in range(actions.count())]
    index = unique_matching_index(texts, account)
    action = actions.nth(index)
    if not action.is_visible():
        raise ExportError(f"Kontoschaltflaeche fuer {account.name} ist nicht sichtbar.")
    return action


def _account_action_text(action: Any) -> str:
    return action.evaluate(
        """(node) => {
            let current = node;
            for (let level = 0; current && level < 8; level++, current = current.parentElement) {
                const text = current.innerText || '';
                if (/DE\\s*\\d/.test(text)) return text;
            }
            return '';
        }"""
    )


def _open_export_dialog(page: Any) -> Any:
    existing = _visible_export_dialog(page)
    if existing is not None:
        return existing

    buttons = page.get_by_role("button", name=re.compile(r"^Exportieren")).filter(
        visible=True
    )
    if buttons.count() < 1:
        raise ExportError("Keine sichtbare Export-Schaltflaeche gefunden.")
    buttons.first.click()
    return _wait_for_export_dialog(page)


def _visible_export_dialog(page: Any) -> Optional[Any]:
    counts = _export_control_counts(page)
    return _last_visible_dialog(page) if counts == (1, 1, 1) else None


def _wait_for_export_dialog(page: Any) -> Any:
    deadline = time.monotonic() + 10
    counts = (0, 0, 0)
    while time.monotonic() < deadline:
        counts = _export_control_counts(page)
        if counts == (1, 1, 1):
            dialog = _last_visible_dialog(page)
            if dialog is not None:
                return dialog
        page.wait_for_timeout(100)
    raise ExportError(
        "Geoeffnetes Exportformular ist nicht eindeutig: "
        f"CSV={counts[0]}, FROM_SEARCH={counts[1]}, Exportieren={counts[2]}."
    )


def _export_control_counts(page: Any) -> tuple[int, int, int]:
    csv_radio = page.locator(
        "input[type='radio'][value='CSV']"
    ).filter(visible=True)
    period_radio = page.locator(
        "input[type='radio'][value='FROM_SEARCH']"
    ).filter(visible=True)
    export_button = page.get_by_role(
        "button", name="Exportieren", exact=True
    ).filter(visible=True)
    return csv_radio.count(), period_radio.count(), export_button.count()


def _last_visible_dialog(page: Any) -> Optional[Any]:
    dialogs = page.locator(
        "[role='dialog'], .modal.show, mat-dialog-container"
    ).filter(visible=True)
    return dialogs.last if dialogs.count() else None


def _select_account(page: Any, dialog: Any, account: AllowedAccount) -> None:
    selector = dialog.locator(
        "mat-select.kf-account-changer-select[role='combobox']"
    ).filter(visible=True)
    if selector.count() != 1:
        raise ExportError("Kontenauswahl im Exportdialog ist nicht eindeutig.")
    selected_text = selector.inner_text()
    if (
        account.name.casefold() in selected_text.casefold()
        and account.iban in normalize_iban(selected_text)
    ):
        return

    selector.focus()
    selector.press("Enter")
    page.locator("[role='option']").filter(visible=True).first.wait_for(
        state="visible", timeout=10_000
    )

    options = page.locator("[role='option']").filter(visible=True)
    texts = [options.nth(index).inner_text() for index in range(options.count())]
    index = unique_matching_index(texts, account)
    option = options.nth(index)
    option.click()

    selected_text = selector.inner_text()
    if account.name.casefold() not in selected_text.casefold():
        raise ExportError(f"Kontowechsel zu {account.name} wurde nicht bestaetigt.")
    if account.iban not in normalize_iban(selected_text):
        raise ExportError(
            f"IBAN-Pruefung nach Kontowechsel zu {account.name} fehlgeschlagen."
        )


def _select_radio(dialog: Any, value: str) -> None:
    radio = dialog.locator(
        f"input[type='radio'][value='{value}']"
    ).filter(visible=True)
    if radio.count() != 1:
        raise ExportError(
            f"Exportoption {value} wurde {radio.count()}-mal statt einmal gefunden."
        )
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and not radio.is_enabled():
        time.sleep(0.2)
    if not radio.is_enabled():
        raise ExportError(f"Exportoption {value} blieb deaktiviert.")
    radio.check(force=True)
    if not radio.is_checked():
        raise ExportError(f"Exportoption {value} wurde nicht aktiviert.")


def _close_export_dialog(page: Any) -> None:
    close_button = page.get_by_role(
        "button", name="Export schließen", exact=True
    ).filter(visible=True)
    if close_button.count() == 1:
        close_button.click()

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if _visible_export_dialog(page) is None:
            return
        page.wait_for_timeout(100)
    raise ExportError("Exportdialog konnte nach dem Download nicht geschlossen werden.")


def _remove_partial_run(
    run_dir: Path, output_dir: Path, logger: logging.Logger
) -> None:
    resolved_run = run_dir.resolve()
    resolved_output = output_dir.resolve()
    if resolved_run.parent != resolved_output:
        logger.error("Teil-Export wird nicht geloescht: unerwarteter Pfad.")
        return
    try:
        shutil.rmtree(resolved_run)
        logger.info("Unvollstaendiger Exportlauf wurde entfernt.")
    except OSError as exc:
        logger.warning("Unvollstaendiger Exportlauf konnte nicht entfernt werden: %s", exc)
