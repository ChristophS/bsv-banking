from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)


def ensure_private_directory(path: Path) -> Path:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    _set_mode(path, 0o700)
    return path


def protect_file(path: Path) -> None:
    if path.exists():
        _set_mode(path, 0o600)


def redact_urls(message: str) -> str:
    return URL_PATTERN.sub(lambda match: _redact_url(match.group(0)), message)


def _redact_url(value: str) -> str:
    trailing = ""
    while value and value[-1] in ".,);]":
        trailing = value[-1] + trailing
        value = value[:-1]

    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        return value + trailing

    hostname = parsed.hostname or ""
    netloc = hostname
    if parsed.port:
        netloc = f"{hostname}:{parsed.port}"
    redacted = urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))
    if parsed.query or parsed.fragment:
        redacted += "?<redacted>"
    return redacted + trailing


def _set_mode(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        # Windows and some mounted filesystems only partially support POSIX modes.
        pass
