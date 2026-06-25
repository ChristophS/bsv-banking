from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9 and 3.10
    import tomli as tomllib  # type: ignore[no-redef]


class ConfigError(ValueError):
    """Raised when the local configuration is missing or unsafe."""


@dataclass(frozen=True)
class DetectionConfig:
    success_selector: Optional[str]
    success_url_pattern: Optional[str]
    timeout_seconds: int
    poll_interval_seconds: float
    stable_seconds: float
    success_text_pattern: Optional[str] = None


@dataclass(frozen=True)
class CredentialsConfig:
    mode: str
    env_file: Optional[Path]
    username_variable: Optional[str]
    password_variable: Optional[str]
    username_selector: Optional[str]
    password_selector: Optional[str]
    submit_selector: Optional[str]
    username_submit_selector: Optional[str] = None


@dataclass(frozen=True)
class ExportAccount:
    name: str
    iban: str
    filename: str


@dataclass(frozen=True)
class ExportConfig:
    output_dir: Path
    format: str
    period: str
    download_timeout_seconds: int
    accounts: tuple[ExportAccount, ...] = ()


@dataclass(frozen=True)
class RuntimeConfig:
    profile_dir: Path
    log_dir: Path
    screenshot_dir: Path
    navigation_timeout_seconds: int


@dataclass(frozen=True)
class AppConfig:
    login_url: str
    credentials: CredentialsConfig
    export: ExportConfig
    detection: DetectionConfig
    runtime: RuntimeConfig
    provider: str = "volksbank"


def load_config(path: Path) -> AppConfig:
    config_path = path.expanduser().resolve()
    if not config_path.is_file():
        raise ConfigError(
            f"Konfigurationsdatei fehlt: {config_path}. "
            "Zuerst 'python main.py --init-config' ausfuehren."
        )

    try:
        with config_path.open("rb") as config_file:
            raw = tomllib.load(config_file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigError(f"Konfiguration kann nicht gelesen werden: {exc}") from exc

    bank = _table(raw, "bank")
    credentials = _table(raw, "credentials")
    export = _table(raw, "export")
    detection = _table(raw, "detection")
    runtime = _table(raw, "runtime")

    provider = (_optional_string(bank, "provider") or "volksbank").lower()
    if provider not in {"volksbank", "sparkasse"}:
        raise ConfigError("'bank.provider' muss 'volksbank' oder 'sparkasse' sein.")

    login_url = _required_string(bank, "login_url")
    _validate_login_url(login_url)

    success_selector = _optional_string(detection, "success_selector")
    success_url_pattern = _optional_string(detection, "success_url_pattern")
    success_text_pattern = _optional_string(detection, "success_text_pattern")
    if not success_selector and not success_url_pattern and not success_text_pattern:
        raise ConfigError(
            "Mindestens 'detection.success_selector' oder "
            "'detection.success_url_pattern' oder "
            "'detection.success_text_pattern' muss gesetzt sein."
        )
    for pattern_name, pattern in (
        ("URL", success_url_pattern),
        ("Text", success_text_pattern),
    ):
        if not pattern:
            continue
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ConfigError(
                f"Ungueltiger {pattern_name}-Regulaerausdruck: {exc}"
            ) from exc

    base_dir = config_path.parent
    credentials_config = _credentials_config(credentials, base_dir, provider)
    export_config = _export_config(raw, export, base_dir, provider)
    return AppConfig(
        login_url=login_url,
        credentials=credentials_config,
        export=export_config,
        detection=DetectionConfig(
            success_selector=success_selector,
            success_url_pattern=success_url_pattern,
            timeout_seconds=_positive_int(detection, "timeout_seconds", 300),
            poll_interval_seconds=_positive_number(
                detection, "poll_interval_seconds", 0.5
            ),
            stable_seconds=_positive_number(detection, "stable_seconds", 2.0),
            success_text_pattern=success_text_pattern,
        ),
        runtime=RuntimeConfig(
            profile_dir=_local_path(
                base_dir, runtime.get("profile_dir", ".runtime/session/chromium")
            ),
            log_dir=_local_path(base_dir, runtime.get("log_dir", ".runtime/logs")),
            screenshot_dir=_local_path(
                base_dir, runtime.get("screenshot_dir", ".runtime/screenshots")
            ),
            navigation_timeout_seconds=_positive_int(
                runtime, "navigation_timeout_seconds", 45
            ),
        ),
        provider=provider,
    )


def _export_config(
    raw: Dict[str, Any],
    table: Dict[str, Any],
    base_dir: Path,
    provider: str,
) -> ExportConfig:
    default_format = "CSV" if provider == "volksbank" else "CSV_MT940"
    default_period = "FROM_SEARCH" if provider == "volksbank" else "CURRENT_VIEW"
    export_format = _normalize_export_format(
        _optional_string(table, "format") or default_format
    )
    period = (_optional_string(table, "period") or default_period).upper()

    if provider == "volksbank":
        if export_format != "CSV":
            raise ConfigError(
                "'export.format' muss fuer die Volksbank 'CSV' sein."
            )
        if period != "FROM_SEARCH":
            raise ConfigError(
                "'export.period' muss fuer die Volksbank 'FROM_SEARCH' sein."
            )
    else:
        if export_format != "CSV_MT940":
            raise ConfigError(
                "'export.format' muss fuer die Sparkasse "
                "'Excel (CSV-MT940)' oder 'CSV_MT940' sein."
            )
        if period != "CURRENT_VIEW":
            raise ConfigError(
                "'export.period' muss fuer die Sparkasse 'CURRENT_VIEW' sein."
            )

    accounts = _accounts_config(raw.get("accounts"))
    if provider == "sparkasse" and not accounts:
        raise ConfigError(
            "Fuer die Sparkasse muss mindestens ein '[[accounts]]'-Eintrag "
            "konfiguriert sein."
        )

    return ExportConfig(
        output_dir=_local_path(
            base_dir, table.get("output_dir", ".runtime/exports")
        ),
        format=export_format,
        period=period,
        download_timeout_seconds=_positive_int(
            table, "download_timeout_seconds", 60
        ),
        accounts=accounts,
    )


def _credentials_config(
    table: Dict[str, Any], base_dir: Path, provider: str
) -> CredentialsConfig:
    mode = _optional_string(table, "mode") or "manual"
    if mode not in {"manual", "env"}:
        raise ConfigError("'credentials.mode' muss 'manual' oder 'env' sein.")

    if mode == "manual":
        return CredentialsConfig(
            mode=mode,
            env_file=None,
            username_variable=None,
            password_variable=None,
            username_selector=None,
            password_selector=None,
            submit_selector=None,
            username_submit_selector=None,
        )

    env_file = _local_path(base_dir, table.get("env_file"))
    username_variable = _required_string(table, "username_variable")
    password_variable = _required_string(table, "password_variable")
    _validate_variable_name(username_variable)
    _validate_variable_name(password_variable)

    if provider == "volksbank":
        username_selector = _required_string(table, "username_selector")
        password_selector = _required_string(table, "password_selector")
        submit_selector = _required_string(table, "submit_selector")
        username_submit_selector = None
    else:
        username_selector = (
            _optional_string(table, "username_selector")
            or "input[autocomplete='username']:visible"
        )
        password_selector = (
            _optional_string(table, "password_selector")
            or "input[type='password']:visible"
        )
        username_submit_selector = (
            _optional_string(table, "username_submit_selector")
            or (
                "input[type='submit'][title='Weiter']:visible, "
                "input[type='submit'][value='Weiter']:visible"
            )
        )
        submit_selector = (
            _optional_string(table, "submit_selector")
            or (
                "input[type='submit'][title='Anmelden']:visible, "
                "input[type='submit'][value='Anmelden']:visible, "
                "button[type='submit']:visible"
            )
        )

    return CredentialsConfig(
        mode=mode,
        env_file=env_file,
        username_variable=username_variable,
        password_variable=password_variable,
        username_selector=username_selector,
        password_selector=password_selector,
        submit_selector=submit_selector,
        username_submit_selector=username_submit_selector,
    )


def _normalize_export_format(value: str) -> str:
    normalized = re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")
    if normalized in {"EXCEL_CSV_MT940", "CSV_MT940"}:
        return "CSV_MT940"
    return normalized


def _accounts_config(value: Any) -> tuple[ExportAccount, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ConfigError("'accounts' muss eine Liste von TOML-Tabellen sein.")

    accounts = []
    seen_ibans = set()
    seen_filenames = set()
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ConfigError(f"'accounts[{index}]' muss eine TOML-Tabelle sein.")
        name = _required_string(item, "name")
        iban = re.sub(r"[^A-Za-z0-9]", "", _required_string(item, "iban")).upper()
        filename = _required_string(item, "filename")

        if not re.fullmatch(r"DE[0-9]{20}", iban):
            raise ConfigError(
                f"Ungueltige deutsche IBAN in 'accounts[{index}]'."
            )
        if Path(filename).name != filename or not filename.lower().endswith(".csv"):
            raise ConfigError(
                f"'accounts[{index}].filename' muss ein einfacher CSV-Dateiname sein."
            )
        filename_key = filename.casefold()
        if iban in seen_ibans:
            raise ConfigError(f"Doppelte IBAN in 'accounts[{index}]'.")
        if filename_key in seen_filenames:
            raise ConfigError(f"Doppelter Dateiname in 'accounts[{index}]'.")

        seen_ibans.add(iban)
        seen_filenames.add(filename_key)
        accounts.append(ExportAccount(name=name, iban=iban, filename=filename))

    return tuple(accounts)


def _table(raw: Dict[str, Any], name: str) -> Dict[str, Any]:
    value = raw.get(name, {})
    if not isinstance(value, dict):
        raise ConfigError(f"'{name}' muss eine TOML-Tabelle sein.")
    return value


def _required_string(table: Dict[str, Any], key: str) -> str:
    value = _optional_string(table, key)
    if not value:
        raise ConfigError(f"'{key}' fehlt oder ist leer.")
    return value


def _optional_string(table: Dict[str, Any], key: str) -> Optional[str]:
    value = table.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ConfigError(f"'{key}' muss eine Zeichenkette sein.")
    stripped = value.strip()
    return stripped or None


def _positive_int(table: Dict[str, Any], key: str, default: int) -> int:
    value = table.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ConfigError(f"'{key}' muss eine positive Ganzzahl sein.")
    return value


def _positive_number(table: Dict[str, Any], key: str, default: float) -> float:
    value = table.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ConfigError(f"'{key}' muss eine positive Zahl sein.")
    return float(value)


def _local_path(base_dir: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError("Laufzeitpfade muessen nicht-leere Zeichenketten sein.")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def _validate_variable_name(value: str) -> None:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise ConfigError(f"Ungueltiger Umgebungsvariablenname: {value}")


def _validate_login_url(login_url: str) -> None:
    parsed = urlsplit(login_url)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        raise ConfigError("Die Login-URL muss eine vollstaendige HTTPS-URL sein.")
    if parsed.username or parsed.password:
        raise ConfigError("Die Login-URL darf keine Zugangsdaten enthalten.")
    if parsed.hostname.endswith(".example.invalid"):
        raise ConfigError(
            "Die Beispiel-Login-URL muss in config.toml ersetzt werden."
        )
