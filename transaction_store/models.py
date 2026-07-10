from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True)
class AccountDefinition:
    provider: str
    name: str
    number: str
    filename: str


@dataclass(frozen=True)
class ParsedTransaction:
    transaction_id: str
    fingerprint: str
    occurrence: int
    provider: str
    account_name: str
    account_number: str
    booking_date: str
    value_date: str
    counterparty: str
    amount: Decimal
    account_balance: Decimal | None
    currency: str
    booking_text: str
    purpose: str
    counterparty_account: str
    creditor_id: str
    mandate_reference: str
    source_info: str
    raw_fields: Mapping[str, str]
    source_row_number: int


@dataclass(frozen=True)
class ParsedFile:
    path: Path
    encoding: str
    delimiter: str
    sha256: str
    account: AccountDefinition
    transactions: tuple[ParsedTransaction, ...]
    account_balance: Decimal | None
    balance_as_of: str | None
    balance_currency: str | None


@dataclass(frozen=True)
class TransactionSplit:
    split_id: str
    transaction_id: str
    amount_minor: int
    sort_order: int = 0
    description: str = ""
    transaction_type: str = ""
    top_category: str = ""
    sub_category: str = ""
    sphere: str = ""
    professional_description: str = ""
    vorgangs_id: str | None = None
    created_at: str = ""
    updated_at: str = ""
