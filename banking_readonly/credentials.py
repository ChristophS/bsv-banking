from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .config import CredentialsConfig


class CredentialError(RuntimeError):
    """Raised when local credentials cannot be loaded safely."""


@dataclass(frozen=True)
class Credentials:
    username: str = field(repr=False)
    password: str = field(repr=False)


def load_credentials(config: CredentialsConfig) -> Credentials:
    if config.mode != "env" or config.env_file is None:
        raise CredentialError("Credential-Laden ist nur im Modus 'env' moeglich.")

    env_path = Path(config.env_file)
    if not env_path.is_file():
        raise CredentialError(f"Secrets-Datei nicht gefunden: {env_path}")

    try:
        from dotenv import dotenv_values
    except ModuleNotFoundError as exc:
        raise CredentialError(
            "python-dotenv fehlt. Abhaengigkeiten aus requirements.txt installieren."
        ) from exc

    try:
        values = dotenv_values(
            dotenv_path=env_path,
            encoding="utf-8-sig",
            interpolate=False,
        )
    except OSError as exc:
        raise CredentialError(f"Secrets-Datei kann nicht gelesen werden: {exc}") from exc

    username = _required_secret(values, config.username_variable)
    password = _required_secret(values, config.password_variable)
    return Credentials(username=username, password=password)


def _required_secret(values: dict, variable_name: Optional[str]) -> str:
    if not variable_name:
        raise CredentialError("Name der Credential-Variable fehlt.")
    value = values.get(variable_name)
    if not isinstance(value, str) or not value:
        raise CredentialError(
            f"Credential-Variable '{variable_name}' fehlt oder ist leer."
        )
    return value
