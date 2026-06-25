from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Mapping

from .security import protect_file


BALANCE_SNAPSHOT_FILENAME = "account_balances.json"


@dataclass(frozen=True)
class AccountBalanceObservation:
    account_name: str
    account_number: str
    balance: Decimal
    currency: str
    captured_at: datetime


def write_balance_snapshot(
    run_dir: Path,
    provider: str,
    observations: Mapping[str, AccountBalanceObservation],
) -> Path:
    payload = {
        "version": 1,
        "provider": provider,
        "accounts": {
            account_number: {
                "name": observation.account_name,
                "balance": format(observation.balance, "f"),
                "currency": observation.currency,
                "captured_at": observation.captured_at.isoformat(),
            }
            for account_number, observation in sorted(observations.items())
        },
    }
    path = run_dir / BALANCE_SNAPSHOT_FILENAME
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)
    protect_file(path)
    return path


def load_balance_snapshot(
    run_dir: Path,
    expected_provider: str,
) -> dict[str, AccountBalanceObservation]:
    path = run_dir / BALANCE_SNAPSHOT_FILENAME
    if not path.exists():
        return {}

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Kontostandsdatei ist unlesbar: {path}") from exc

    if payload.get("version") != 1:
        raise RuntimeError(f"Unbekannte Version der Kontostandsdatei: {path}")
    if payload.get("provider") != expected_provider:
        raise RuntimeError(
            f"Kontostandsdatei gehoert nicht zu {expected_provider}: {path}"
        )

    raw_accounts = payload.get("accounts")
    if not isinstance(raw_accounts, dict):
        raise RuntimeError(f"Kontostandsdatei enthaelt keine Konten: {path}")

    observations: dict[str, AccountBalanceObservation] = {}
    for account_number, raw in raw_accounts.items():
        if not isinstance(account_number, str) or not isinstance(raw, dict):
            raise RuntimeError(f"Ungueltiger Kontostandseintrag: {path}")
        try:
            balance = Decimal(str(raw["balance"]))
            captured_at = datetime.fromisoformat(str(raw["captured_at"]))
            account_name = str(raw["name"])
            currency = str(raw["currency"]).upper()
        except (KeyError, ValueError, InvalidOperation) as exc:
            raise RuntimeError(f"Ungueltiger Kontostandseintrag: {path}") from exc
        if not account_name or not currency:
            raise RuntimeError(f"Unvollstaendiger Kontostandseintrag: {path}")
        observations[account_number] = AccountBalanceObservation(
            account_name=account_name,
            account_number=account_number,
            balance=balance,
            currency=currency,
            captured_at=captured_at,
        )

    return observations
