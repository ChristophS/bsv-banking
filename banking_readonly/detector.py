from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Any, Optional

from .config import DetectionConfig


class LoginTimeoutError(TimeoutError):
    """Raised when no configured success criterion becomes stable."""


class BrowserClosedError(RuntimeError):
    """Raised when the user closes all browser pages during the test."""


@dataclass(frozen=True)
class DetectionResult:
    criterion: str
    page: Any = None


def url_matches(pattern: Optional[str], url: str) -> bool:
    return bool(pattern and re.search(pattern, url))


def wait_for_success(context: Any, config: DetectionConfig) -> DetectionResult:
    deadline = time.monotonic() + config.timeout_seconds
    candidate_key: Optional[tuple[int, str]] = None
    candidate_since = 0.0

    while time.monotonic() < deadline:
        pages = [page for page in context.pages if not page.is_closed()]
        if not pages:
            raise BrowserClosedError("Alle Browserfenster wurden geschlossen.")

        current_candidate: Optional[tuple[int, str]] = None
        for page in pages:
            criterion = success_criterion(page, config)
            if criterion:
                current_candidate = (id(page), criterion)
                break

        now = time.monotonic()
        if current_candidate is None:
            candidate_key = None
            candidate_since = 0.0
        elif current_candidate != candidate_key:
            candidate_key = current_candidate
            candidate_since = now
        elif now - candidate_since >= config.stable_seconds:
            matched_page = next(
                page for page in pages if id(page) == current_candidate[0]
            )
            return DetectionResult(
                criterion=current_candidate[1],
                page=matched_page,
            )

        time.sleep(config.poll_interval_seconds)

    raise LoginTimeoutError(
        f"Login wurde innerhalb von {config.timeout_seconds} Sekunden "
        "nicht anhand der konfigurierten Kriterien erkannt."
    )


def success_criterion(page: Any, config: DetectionConfig) -> Optional[str]:
    if _selector_is_visible(page, config.success_selector):
        return "stabiler DOM-Selektor"
    if url_matches(config.success_url_pattern, page.url):
        return "URL-Muster"
    if _text_matches(page, config.success_text_pattern):
        return "Text-Muster"
    return None


def _selector_is_visible(page: Any, selector: Optional[str]) -> bool:
    if not selector:
        return False
    try:
        return page.locator(selector).first.is_visible(timeout=250)
    except Exception:
        return False


def _text_matches(page: Any, pattern: Optional[str]) -> bool:
    if not pattern:
        return False
    try:
        body_text = page.locator("body").inner_text(timeout=250)
        return bool(re.search(pattern, body_text))
    except Exception:
        # Navigation can temporarily detach the document or leave it without
        # a body. The polling loop retries until the configured deadline.
        return False
