from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .security import ensure_private_directory, protect_file, redact_urls


class SensitiveDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_urls(record.getMessage())
        record.args = ()
        return True


class RedactingFormatter(logging.Formatter):
    def formatException(self, exc_info: object) -> str:
        return redact_urls(super().formatException(exc_info))


def configure_logging(log_dir: Path) -> tuple[logging.Logger, Path]:
    ensure_private_directory(log_dir)
    log_path = log_dir / "onlinebanking-test.log"

    logger = logging.getLogger("banking_readonly")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = RedactingFormatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    data_filter = SensitiveDataFilter()

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(data_filter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(data_filter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    protect_file(log_path)
    return logger, log_path
