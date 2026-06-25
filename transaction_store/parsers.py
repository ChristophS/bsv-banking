from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Mapping

from .models import AccountDefinition, ParsedFile, ParsedTransaction


class TransactionParseError(ValueError):
    """Raised when a bank export cannot be normalized safely."""


VOLKSBANK_HEADERS = (
    "Bezeichnung Auftragskonto",
    "IBAN Auftragskonto",
    "BIC Auftragskonto",
    "Bankname Auftragskonto",
    "Buchungstag",
    "Valutadatum",
    "Name Zahlungsbeteiligter",
    "IBAN Zahlungsbeteiligter",
    "BIC (SWIFT-Code) Zahlungsbeteiligter",
    "Buchungstext",
    "Verwendungszweck",
    "Betrag",
    "Waehrung",
    "Saldo nach Buchung",
    "Bemerkung",
    "Gekennzeichneter Umsatz",
    "Glaeubiger ID",
    "Mandatsreferenz",
)

VOLKSBANK_LEGACY_HEADERS = (
    "Bezeichnung Auftragskonto",
    "IBAN Auftragskonto",
    "BIC Auftragskonto",
    "Bankname Auftragskonto",
    "Buchungstag",
    "Valutadatum",
    "Name Zahlungsbeteiligter",
    "IBAN Zahlungsbeteiligter",
    "BIC (SWIFT-Code) Zahlungsbeteiligter",
    "Buchungstext",
    "Verwendungszweck",
    "Betrag",
    "Waehrung",
    "Saldo nach Buchung",
    "Bemerkung",
    "Kategorie",
    "Steuerrelevant",
    "Glaeubiger ID",
    "Mandatsreferenz",
)

SPARKASSE_HEADERS = (
    "Auftragskonto",
    "Buchungstag",
    "Valutadatum",
    "Buchungstext",
    "Verwendungszweck",
    "Beguenstigter/Zahlungspflichtiger",
    "Kontonummer",
    "BLZ",
    "Betrag",
    "Waehrung",
    "Info",
)

SPARKASSE_LEGACY_HEADERS = (
    "Auftragskonto",
    "Buchungstag",
    "Valutadatum",
    "Buchungstext",
    "Verwendungszweck",
    "Glaeubiger ID",
    "Mandatsreferenz",
    "Kundenreferenz (End-to-End)",
    "Sammlerreferenz",
    "Lastschrift Ursprungsbetrag",
    "Auslagenersatz Ruecklastschrift",
    "Beguenstigter/Zahlungspflichtiger",
    "Kontonummer/IBAN",
    "BIC (SWIFT-Code)",
    "Betrag",
    "Waehrung",
    "Info",
)

SPARKASSE_CATEGORY_HEADERS = (
    "Auftragskonto",
    "Buchungstag",
    "Valutadatum",
    "Buchungstext",
    "Verwendungszweck",
    "Beguenstigter/Zahlungspflichtiger",
    "Kontonummer/IBAN",
    "BIC (SWIFT-Code)",
    "Betrag",
    "Waehrung",
    "Info",
    "Kategorie",
)

SUPPORTED_HEADERS = {
    "volksbank": (VOLKSBANK_HEADERS, VOLKSBANK_LEGACY_HEADERS),
    "sparkasse": (
        SPARKASSE_HEADERS,
        SPARKASSE_LEGACY_HEADERS,
        SPARKASSE_CATEGORY_HEADERS,
    ),
}


def parse_export(
    path: Path,
    account: AccountDefinition,
    *,
    account_balance: Decimal | None = None,
    balance_as_of: str | None = None,
    balance_currency: str | None = None,
) -> ParsedFile:
    raw = path.read_bytes()
    text, encoding = _decode(raw)
    reader = csv.DictReader(text.splitlines(), delimiter=";")
    headers = tuple(reader.fieldnames or ())
    if headers not in SUPPORTED_HEADERS.get(account.provider, ()):
        raise TransactionParseError(
            f"Unerwartetes CSV-Schema in {path.name}: {headers}"
        )

    rows = list(reader)
    parsed_rows = []
    for row_number, row in enumerate(rows, start=2):
        normalized_row = {
            key: _normalize_text(value)
            for key, value in row.items()
            if key is not None
        }
        if (
            account.provider == "sparkasse"
            and _is_pending_sparkasse_row(normalized_row)
        ):
            continue
        fields = (
            _parse_volksbank_row(normalized_row, account)
            if account.provider == "volksbank"
            else _parse_sparkasse_row(normalized_row, account)
        )
        parsed_rows.append((row_number, normalized_row, fields))

    if account.provider == "volksbank":
        _calculate_and_validate_volksbank_balances(parsed_rows, path)
        if (
            account_balance is not None
            and parsed_rows
            and parsed_rows[0][2]["account_balance"] != account_balance
        ):
            raise TransactionParseError(
                "Kontostand der Volksbank-Kontouebersicht passt nicht zum "
                f"neuesten CSV-Saldo in {path.name}."
            )
    elif account_balance is not None:
        _calculate_sparkasse_balances_from_anchor(
            parsed_rows,
            account_balance,
        )

    occurrence_counts: Counter[str] = Counter()
    parsed = []
    for row_number, normalized_row, fields in parsed_rows:
        identity_fields = {
            key: value
            for key, value in fields.items()
            if key not in {"source_info", "account_balance"}
        }
        fingerprint = _fingerprint(
            {
                "provider": account.provider,
                "account_number": account.number,
                **identity_fields,
            }
        )
        occurrence_counts[fingerprint] += 1
        occurrence = occurrence_counts[fingerprint]
        transaction_id = _transaction_id(fingerprint, occurrence)
        parsed.append(
            ParsedTransaction(
                transaction_id=transaction_id,
                fingerprint=fingerprint,
                occurrence=occurrence,
                provider=account.provider,
                account_name=account.name,
                account_number=account.number,
                source_row_number=row_number,
                raw_fields=normalized_row,
                **fields,
            )
        )

    parsed_account_balance = (
        parsed[0].account_balance
        if parsed and parsed[0].account_balance is not None
        else account_balance
    )
    parsed_balance_as_of = (
        balance_as_of
        if parsed_account_balance is not None and balance_as_of
        else (
            parsed[0].booking_date
            if parsed and parsed_account_balance is not None
            else None
        )
    )
    parsed_balance_currency = (
        balance_currency.upper()
        if parsed_account_balance is not None and balance_currency
        else (
            parsed[0].currency
            if parsed and parsed_account_balance is not None
            else None
        )
    )
    if parsed_account_balance is not None and parsed_balance_currency is None:
        raise TransactionParseError(
            f"Kontostandswaehrung fehlt fuer {path.name}."
        )
    if parsed_balance_currency and any(
        transaction.currency != parsed_balance_currency
        for transaction in parsed
    ):
        raise TransactionParseError(
            f"Kontostandswaehrung passt nicht zu den Umsaetzen in {path.name}."
        )
    return ParsedFile(
        path=path,
        encoding=encoding,
        delimiter=";",
        sha256=hashlib.sha256(raw).hexdigest(),
        account=account,
        transactions=tuple(parsed),
        account_balance=parsed_account_balance,
        balance_as_of=parsed_balance_as_of,
        balance_currency=parsed_balance_currency,
    )


def detect_export_account(path: Path) -> tuple[str, str] | None:
    raw = path.read_bytes()
    text, _ = _decode(raw)
    reader = csv.DictReader(text.splitlines(), delimiter=";")
    headers = tuple(reader.fieldnames or ())
    provider = next(
        (
            name
            for name, supported in SUPPORTED_HEADERS.items()
            if headers in supported
        ),
        None,
    )
    if provider is None:
        return None

    first_row = next(reader, None)
    if first_row is not None:
        account_field = (
            "IBAN Auftragskonto"
            if provider == "volksbank"
            else "Auftragskonto"
        )
        account_number = _normalize_account(first_row.get(account_field, ""))
        if account_number:
            return provider, account_number

    match = re.search(r"DE\d{20}", path.name, flags=re.IGNORECASE)
    if match:
        return provider, match.group(0).upper()
    return None


def _parse_volksbank_row(
    row: Mapping[str, str],
    account: AccountDefinition,
) -> dict:
    source_account = _normalize_account(row["IBAN Auftragskonto"])
    _validate_account(source_account, account)
    return {
        "booking_date": _parse_date(row["Buchungstag"], "%d.%m.%Y"),
        "value_date": _parse_date(row["Valutadatum"], "%d.%m.%Y"),
        "counterparty": row["Name Zahlungsbeteiligter"],
        "amount": _parse_amount(row["Betrag"]),
        "account_balance": None,
        "currency": row["Waehrung"].upper(),
        "booking_text": row["Buchungstext"],
        "purpose": row["Verwendungszweck"],
        "counterparty_account": _normalize_account(
            row["IBAN Zahlungsbeteiligter"]
        ),
        "creditor_id": row["Glaeubiger ID"],
        "mandate_reference": row["Mandatsreferenz"],
        "source_info": " | ".join(
            value
            for value in (
                row.get("Bemerkung", ""),
                row.get("Gekennzeichneter Umsatz", ""),
                row.get("Kategorie", ""),
                row.get("Steuerrelevant", ""),
            )
            if value
        ),
    }


def _parse_sparkasse_row(
    row: Mapping[str, str],
    account: AccountDefinition,
) -> dict:
    source_account = _normalize_account(row["Auftragskonto"])
    _validate_account(source_account, account)
    value_date = _parse_short_date(row["Valutadatum"])
    booking_date = (
        _parse_short_date(row["Buchungstag"])
        if row["Buchungstag"]
        else value_date
    )
    return {
        "booking_date": booking_date,
        "value_date": value_date,
        "counterparty": row["Beguenstigter/Zahlungspflichtiger"],
        "amount": _parse_amount(row["Betrag"]),
        "account_balance": None,
        "currency": row["Waehrung"].upper(),
        "booking_text": row["Buchungstext"],
        "purpose": row["Verwendungszweck"],
        "counterparty_account": _normalize_account(
            row.get("Kontonummer/IBAN", row.get("Kontonummer", ""))
        ),
        "creditor_id": "",
        "mandate_reference": "",
        "source_info": " | ".join(
            value
            for value in (row.get("Info", ""), row.get("Kategorie", ""))
            if value
        ),
    }


def _is_pending_sparkasse_row(row: Mapping[str, str]) -> bool:
    return "vorgemerkt" in row.get("Info", "").casefold()


def _calculate_and_validate_volksbank_balances(
    parsed_rows: list[tuple[int, dict[str, str], dict]],
    path: Path,
) -> None:
    if not parsed_rows:
        return

    _, latest_raw, latest_fields = parsed_rows[0]
    current_balance = _parse_amount(latest_raw["Saldo nach Buchung"])
    latest_fields["account_balance"] = current_balance

    previous_fields = latest_fields
    for row_number, raw, fields in parsed_rows[1:]:
        current_balance -= previous_fields["amount"]
        reported_balance = _parse_amount(raw["Saldo nach Buchung"])
        if reported_balance != current_balance:
            raise TransactionParseError(
                "Inkonsistente Kontostandskette in "
                f"{path.name}, Zeile {row_number}: "
                f"berechnet {current_balance:.2f}, "
                f"gemeldet {reported_balance:.2f}."
            )
        fields["account_balance"] = current_balance
        previous_fields = fields


def _calculate_sparkasse_balances_from_anchor(
    parsed_rows: list[tuple[int, dict[str, str], dict]],
    account_balance: Decimal,
) -> None:
    current_balance = account_balance
    previous_booked_fields = None
    for _, _, fields in parsed_rows:
        if "vorgemerkt" in fields["source_info"].casefold():
            fields["account_balance"] = None
            continue
        if previous_booked_fields is not None:
            current_balance -= previous_booked_fields["amount"]
        fields["account_balance"] = current_balance
        previous_booked_fields = fields


def _fingerprint(fields: Mapping[str, object]) -> str:
    payload = {
        key: _decimal_string(value) if isinstance(value, Decimal) else value
        for key, value in fields.items()
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _transaction_id(fingerprint: str, occurrence: int) -> str:
    payload = f"transaction-id-v1|{fingerprint}|{occurrence}".encode("ascii")
    return "tx_" + hashlib.sha256(payload).hexdigest()


def _decode(raw: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise TransactionParseError("CSV-Encoding ist weder UTF-8 noch Windows-1252.")


def _parse_date(value: str, date_format: str) -> str:
    try:
        return datetime.strptime(value, date_format).date().isoformat()
    except ValueError as exc:
        raise TransactionParseError(f"Ungueltiges Buchungsdatum: {value}") from exc


def _parse_short_date(value: str) -> str:
    try:
        day, month, year = (int(part) for part in value.split("."))
        return datetime(2000 + year, month, day).date().isoformat()
    except (TypeError, ValueError) as exc:
        raise TransactionParseError(f"Ungueltiges Buchungsdatum: {value}") from exc


def _parse_amount(value: str) -> Decimal:
    normalized = value.replace(".", "").replace(",", ".")
    try:
        return Decimal(normalized).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise TransactionParseError(f"Ungueltiger Betrag: {value}") from exc


def _validate_account(source_account: str, account: AccountDefinition) -> None:
    if source_account != account.number:
        raise TransactionParseError(
            f"Kontonummer in CSV passt nicht zur Allowlist fuer {account.filename}."
        )


def _normalize_account(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def _normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFKC", value).split())


def _decimal_string(value: Decimal) -> str:
    return format(value, ".2f")
