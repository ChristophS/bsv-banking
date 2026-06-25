from __future__ import annotations

import copy
import csv
import hashlib
import json
import logging
import os
import re
import threading
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

from banking_readonly.security import ensure_private_directory, protect_file

from .player_premiums import DFBNET_RESULT_DIR, PROJECT_ROOT, SECRETS_PATH


DFBNET_VEREIN_LOGIN_URL = "https://verein.dfbnet.org/login/23040090"
DFBNET_VEREIN_PROFILE_DIR = (
    PROJECT_ROOT / ".runtime" / "session" / "dfbnet-verein-chromium"
)
PREMIUM_LATEST_PATH = DFBNET_RESULT_DIR / "spieler_praemien_zuletzt.json"
PLAYER_PAYMENT_RESULT_DIR = PROJECT_ROOT / ".runtime" / "dfbnet" / "player_payments"
DEFAULT_DECKEL_LIST_PATH = Path(
    os.environ.get(
        "BSV_DECKELLISTE_PATH",
        r"C:\Users\chsue\OneDrive\Dokumente\Getränkeliste BSV Vereinsheim.xlsx",
    )
)
MATCH_SIMILARITY_THRESHOLD = 0.72
MATCH_AMBIGUITY_MARGIN = 0.08
OFFSET_MATCH_THRESHOLD = 0.78
OFFSET_AMBIGUITY_MARGIN = 0.05
_PAYMENT_SESSION_LOCK = threading.RLock()
_CURRENT_PRIVATE_RESULT: dict[str, Any] | None = None

MONEY_QUANT = Decimal("0.01")
XLSX_NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

PREMIUM_TRANSACTION_CLASSIFICATION = {
    "transaction_type": "Prämien",
    "top_category": "Spielbetrieb",
    "sub_category": "Spielerprämien",
    "sphere": "Ideeller Bereich",
}
DECKEL_TRANSACTION_CLASSIFICATION = {
    "transaction_type": "Verkauf Speisen und Getränke",
    "top_category": "Vereinsheim",
    "sub_category": "Speisen und Getränke",
    "sphere": "wirtschaftlicher Geschäftsbetrieb",
}

IBAN_LENGTHS = {
    "AD": 24,
    "AE": 23,
    "AL": 28,
    "AT": 20,
    "AZ": 28,
    "BA": 20,
    "BE": 16,
    "BG": 22,
    "BH": 22,
    "BI": 27,
    "BR": 29,
    "BY": 28,
    "CH": 21,
    "CR": 22,
    "CY": 28,
    "CZ": 24,
    "DE": 22,
    "DJ": 27,
    "DK": 18,
    "DO": 28,
    "EE": 20,
    "EG": 29,
    "ES": 24,
    "FI": 18,
    "FK": 18,
    "FO": 18,
    "FR": 27,
    "GB": 22,
    "GE": 22,
    "GI": 23,
    "GL": 18,
    "GR": 27,
    "GT": 28,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IL": 23,
    "IQ": 23,
    "IS": 26,
    "IT": 27,
    "JO": 30,
    "KZ": 20,
    "KW": 30,
    "LB": 28,
    "LC": 32,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "LY": 25,
    "MC": 27,
    "MD": 24,
    "ME": 22,
    "MK": 19,
    "MN": 20,
    "MR": 27,
    "MT": 31,
    "MU": 30,
    "NI": 32,
    "NL": 18,
    "NO": 15,
    "OM": 23,
    "PK": 24,
    "PL": 28,
    "PS": 29,
    "PT": 25,
    "QA": 29,
    "RO": 24,
    "RS": 22,
    "SA": 24,
    "SC": 31,
    "SD": 18,
    "SE": 24,
    "SI": 19,
    "SK": 24,
    "SM": 27,
    "SO": 23,
    "ST": 25,
    "SV": 28,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "VA": 22,
    "VG": 24,
    "XK": 20,
    "YE": 30,
}


class PlayerPaymentError(RuntimeError):
    pass


@dataclass(frozen=True)
class MemberCandidate:
    member_id: str
    surname: str
    first_name: str
    detail_url: str

    @property
    def display_name(self) -> str:
        return _clean_text(f"{self.first_name} {self.surname}")

    @property
    def source_order_name(self) -> str:
        return _clean_text(f"{self.surname} {self.first_name}")


def run_player_payment_review(
    premium_result: dict[str, Any] | None = None,
    deckel_path: str | None = None,
) -> dict[str, Any]:
    result = premium_result or load_latest_premium_result()
    players = eligible_premium_players(result)
    if not players:
        raise PlayerPaymentError(
            "Die Prämienauswertung enthält keine auszuzahlenden Spieler."
        )
    username, password = _load_credentials()
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise PlayerPaymentError(
            "Playwright fehlt. Abhängigkeiten aus requirements.txt installieren."
        ) from exc

    ensure_private_directory(DFBNET_VEREIN_PROFILE_DIR)
    logger = logging.getLogger(__name__)
    context = None
    page = None
    try:
        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(DFBNET_VEREIN_PROFILE_DIR),
                headless=True,
                accept_downloads=False,
                viewport=None,
            )
            page = _fresh_page(context)
            page.set_default_timeout(30_000)
            _login(page, username, password)
            username = password = ""

            private_rows = []
            for player in players:
                private_rows.append(
                    _resolve_player_payment(page, player)
                )
            deckel_path_text = _clean_text(deckel_path or str(DEFAULT_DECKEL_LIST_PATH))
            deckel_positions: list[dict[str, Any]] = []
            deckel_debtors: list[dict[str, Any]] = []
            warnings: list[str] = []
            try:
                deckel_positions = load_deckel_list_positions(deckel_path_text)
                _preview_deckel_assignments(deckel_positions, private_rows)
                deckel_debtors = _resolve_deckel_debtors(
                    page,
                    deckel_positions,
                    private_rows,
                )
            except PlayerPaymentError as exc:
                warnings.append(str(exc))

            generated_at = datetime.now(timezone.utc).isoformat()
            private_result = {
                "season": result.get("season", ""),
                "generated_at": generated_at,
                "premium_generated_at": result.get("generated_at", ""),
                "teams": _premium_team_definitions(result),
                "players": private_rows,
                "deckel_debtors": deckel_debtors,
                "warnings": warnings,
                "offset_configuration": {
                    "deckel_path": deckel_path_text,
                    "deckel_positions": deckel_positions,
                    "updated_at": generated_at,
                },
            }
            _set_current_private_result(private_result)
            public_result = _public_review(private_result)
            return public_result
    except PlayerPaymentError:
        _save_error_screenshot(page, logger)
        raise
    except Exception as exc:
        _save_error_screenshot(page, logger)
        raise PlayerPaymentError(
            "Zahlungsdaten konnten nicht vollständig aus DFBnet Verein "
            "ausgelesen werden."
        ) from exc
    finally:
        username = password = ""
        if context is not None:
            try:
                context.close()
            except Exception:
                pass


def load_latest_premium_result() -> dict[str, Any]:
    if not PREMIUM_LATEST_PATH.is_file():
        raise PlayerPaymentError(
            "Es liegt noch keine gespeicherte Spielerprämien-Auswertung vor."
        )
    try:
        result = json.loads(PREMIUM_LATEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlayerPaymentError(
            "Die gespeicherte Spielerprämien-Auswertung ist nicht lesbar."
        ) from exc
    if not isinstance(result, dict):
        raise PlayerPaymentError(
            "Die gespeicherte Spielerprämien-Auswertung ist ungültig."
        )
    return result


def load_current_player_payment_review() -> dict[str, Any] | None:
    private_result = _get_current_private_result()
    return _public_review(private_result) if private_result is not None else None


def clear_player_payment_session() -> None:
    global _CURRENT_PRIVATE_RESULT
    with _PAYMENT_SESSION_LOCK:
        _CURRENT_PRIVATE_RESULT = None


def eligible_premium_players(
    premium_result: dict[str, Any],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for team in premium_result.get("teams", []):
        if not isinstance(team, dict):
            continue
        team_id = str(team.get("team_id", "")).strip()
        team_label = str(team.get("label", "")).strip()
        for player in team.get("players", []):
            if not isinstance(player, dict):
                continue
            name = _clean_text(player.get("name", ""))
            try:
                premium_total = float(player.get("premium_total") or 0)
            except (TypeError, ValueError):
                continue
            if not name or premium_total <= 0:
                continue
            key = name.casefold()
            entry = grouped.setdefault(
                key,
                {
                    "premium_name": name,
                    "premium_total": 0.0,
                    "teams": [],
                },
            )
            entry["premium_total"] = round(
                float(entry["premium_total"]) + premium_total,
                2,
            )
            team_entry = next(
                (
                    value
                    for value in entry["teams"]
                    if value["team_id"] == team_id
                ),
                None,
            )
            if team_entry is None:
                entry["teams"].append(
                    {
                        "team_id": team_id,
                        "label": team_label,
                        "premium_total": round(premium_total, 2),
                    }
                )
            else:
                team_entry["premium_total"] = round(
                    float(team_entry["premium_total"]) + premium_total,
                    2,
                )
    return sorted(
        grouped.values(),
        key=lambda item: str(item["premium_name"]).casefold(),
    )


def match_member_name(
    premium_name: str,
    candidates: Iterable[MemberCandidate],
) -> dict[str, Any]:
    candidate_list = list(candidates)
    exact = [
        candidate
        for candidate in candidate_list
        if _is_exact_name_match(premium_name, candidate)
    ]
    if len(exact) == 1:
        return _match_result("exakt", "eindeutig_gefunden", 1.0, exact[0])
    if len(exact) > 1:
        return _match_result("mehrdeutig", "manuell_pruefen", 1.0, None, exact)

    normalized = [
        candidate
        for candidate in candidate_list
        if _is_normalized_name_match(premium_name, candidate)
    ]
    if len(normalized) == 1:
        return _match_result(
            "normalisiert",
            "eindeutig_gefunden",
            1.0,
            normalized[0],
        )
    if len(normalized) > 1:
        return _match_result(
            "mehrdeutig",
            "manuell_pruefen",
            1.0,
            None,
            normalized,
        )

    scored = sorted(
        (
            (_name_similarity(premium_name, candidate), candidate)
            for candidate in candidate_list
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    if not scored or scored[0][0] < MATCH_SIMILARITY_THRESHOLD:
        return _match_result("kein_treffer", "nicht_gefunden", 0.0, None)
    top_score, top_candidate = scored[0]
    close_candidates = [
        candidate
        for score, candidate in scored
        if top_score - score < MATCH_AMBIGUITY_MARGIN
    ]
    if len(close_candidates) > 1:
        return _match_result(
            "mehrdeutig",
            "manuell_pruefen",
            top_score,
            None,
            close_candidates,
        )
    return _match_result(
        "ähnlich",
        "manuell_pruefen",
        top_score,
        top_candidate,
    )


def validate_iban(value: str) -> dict[str, Any]:
    raw = str(value or "").upper()
    compact = re.sub(r"\s+", "", raw)
    invalid_characters = sorted(set(re.sub(r"[A-Z0-9]", "", compact)))
    normalized = re.sub(r"[^A-Z0-9]", "", compact)
    country = normalized[:2] if len(normalized) >= 2 else ""
    expected_length = IBAN_LENGTHS.get(country)
    format_valid = bool(re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]+", normalized))
    length_valid = expected_length is not None and len(normalized) == expected_length
    checksum_valid = (
        format_valid
        and length_valid
        and not invalid_characters
        and _iban_mod97(normalized) == 1
    )
    errors = []
    if invalid_characters:
        errors.append("unzulässige_zeichen")
    if not country or expected_length is None:
        errors.append("laendercode_unbekannt")
    if expected_length is not None and not length_valid:
        errors.append("laenge_ungueltig")
    if normalized and not format_valid:
        errors.append("format_ungueltig")
    if format_valid and length_valid and not checksum_valid:
        errors.append("pruefsumme_ungueltig")
    if not normalized:
        errors.append("fehlt")
    return {
        "normalized": normalized,
        "country": country,
        "expected_length": expected_length,
        "valid": bool(
            normalized
            and format_valid
            and length_valid
            and checksum_valid
            and not invalid_characters
        ),
        "errors": list(dict.fromkeys(errors)),
    }


def validate_bic(value: str) -> dict[str, Any]:
    raw = str(value or "").upper()
    compact = re.sub(r"\s+", "", raw)
    invalid_characters = sorted(set(re.sub(r"[A-Z0-9]", "", compact)))
    normalized = re.sub(r"[^A-Z0-9]", "", compact)
    format_valid = bool(
        re.fullmatch(r"[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?", normalized)
    )
    errors = []
    if invalid_characters:
        errors.append("unzulässige_zeichen")
    if normalized and len(normalized) not in {8, 11}:
        errors.append("laenge_ungueltig")
    if normalized and not format_valid:
        errors.append("format_ungueltig")
    if not normalized:
        errors.append("fehlt")
    return {
        "normalized": normalized,
        "country": normalized[4:6] if len(normalized) >= 6 else "",
        "valid": bool(normalized and format_valid and not invalid_characters),
        "errors": list(dict.fromkeys(errors)),
    }


def validate_payment_data(iban: str, bic: str) -> dict[str, Any]:
    iban_result = validate_iban(iban)
    bic_result = validate_bic(bic)
    if (
        iban_result["valid"]
        and bic_result["valid"]
        and iban_result["country"] != bic_result["country"]
    ):
        assignment = "widerspruechlich"
        assignment_detail = "Die Ländercodes von IBAN und BIC unterscheiden sich."
    else:
        assignment = "nicht_geprueft"
        assignment_detail = (
            "Keine verlässliche lokale Bankstammdatenquelle vorhanden."
        )
    return {
        "iban": iban_result,
        "bic": bic_result,
        "iban_bic_assignment": assignment,
        "iban_bic_detail": assignment_detail,
        "valid_for_manual_confirmation": bool(
            iban_result["valid"]
            and bic_result["valid"]
            and assignment != "widerspruechlich"
        ),
    }


def mask_iban(value: str) -> str:
    normalized = re.sub(r"[^A-Z0-9]", "", str(value or "").upper())
    if not normalized:
        return ""
    if len(normalized) <= 8:
        return "*" * len(normalized)
    masked = normalized[:4] + "*" * (len(normalized) - 8) + normalized[-4:]
    return " ".join(
        masked[index : index + 4]
        for index in range(0, len(masked), 4)
    )


def save_manual_player_payment(
    premium_name: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    name = _clean_text(premium_name)
    if not name:
        raise ValueError("Spielername fehlt.")
    if set(payload) != {"account_holder", "iban", "bic"}:
        raise ValueError(
            "Kontoinhaber, IBAN und BIC müssen vollständig angegeben werden."
        )
    account_holder = _manual_text(
        payload.get("account_holder"),
        "Kontoinhaber",
        200,
    )
    iban = _manual_text(payload.get("iban"), "IBAN", 64)
    bic = _manual_text(payload.get("bic"), "BIC", 32)
    validation = validate_payment_data(iban, bic)

    private_result = _get_current_private_result()
    if private_result is None:
        raise PlayerPaymentError(
            "Bitte zuerst die Zahlungsdaten aktuell aus DFBnet abrufen."
        )

    players = private_result.get("players", [])
    player = next(
        (
            item
            for item in players
            if _clean_text(item.get("premium_name", "")).casefold()
            == name.casefold()
        ),
        None,
    )
    if player is None:
        raise LookupError("Spieler wurde in der Prämienauswertung nicht gefunden.")

    updated_at = datetime.now(timezone.utc).isoformat()
    override = {
        "premium_name": str(player.get("premium_name", name)),
        "account_holder": account_holder,
        "iban": validation["iban"]["normalized"],
        "bic": validation["bic"]["normalized"],
        "validation": validation,
        "updated_at": updated_at,
    }
    _apply_manual_override(player, override)
    private_result["generated_at"] = updated_at
    _set_current_private_result(private_result)
    public_result = _public_review(private_result)
    return public_result


def apply_player_payment_offsets(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Verrechnungen muessen als Objekt uebergeben werden.")
    private_result = _get_current_private_result()
    if private_result is None:
        raise PlayerPaymentError(
            "Bitte zuerst die Zahlungsdaten aktuell aus DFBnet abrufen."
        )

    players = _payment_players(private_result)
    for player in players:
        player["offsets"] = []

    use_deckel = payload.get("use_deckel", True) is not False
    deckel_path = _clean_text(
        payload.get("deckel_path") or str(DEFAULT_DECKEL_LIST_PATH)
    )
    if len(deckel_path) > 500:
        raise ValueError("Pfad zur Deckelliste ist zu lang.")
    previous_deckel_path = _clean_text(
        private_result.get("offset_configuration", {}).get("deckel_path", "")
        if isinstance(private_result.get("offset_configuration"), dict)
        else ""
    )
    if previous_deckel_path and previous_deckel_path != deckel_path:
        private_result["deckel_debtors"] = []

    assignment_payload = payload.get("assignments") or {}
    if not isinstance(assignment_payload, dict):
        raise ValueError("Deckellisten-Zuordnungen muessen ein Objekt sein.")

    deckel_positions: list[dict[str, Any]] = []
    if use_deckel:
        deckel_positions = load_deckel_list_positions(deckel_path)
        _preview_deckel_assignments(deckel_positions, players)
        _apply_deckel_offsets(players, deckel_positions, assignment_payload)

    manual_offsets = payload.get("manual_offsets") or []
    if not isinstance(manual_offsets, list):
        raise ValueError("Manuelle Gegenpositionen muessen eine Liste sein.")
    _apply_manual_offsets(players, manual_offsets)

    updated_at = datetime.now(timezone.utc).isoformat()
    for player in players:
        _refresh_player_amounts(player)
    private_result["generated_at"] = updated_at
    private_result["offset_configuration"] = {
        "deckel_path": deckel_path if use_deckel else "",
        "deckel_positions": deckel_positions,
        "updated_at": updated_at,
    }
    _set_current_private_result(private_result)
    return _public_review(private_result)


def export_player_payment_files(
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if payload is not None and not isinstance(payload, dict):
        raise ValueError("Exportoptionen muessen als Objekt uebergeben werden.")
    private_result = _get_current_private_result()
    if private_result is None:
        raise PlayerPaymentError(
            "Bitte zuerst die Zahlungsdaten aktuell aus DFBnet abrufen."
        )

    players = _payment_players(private_result)
    transfer_rows: list[dict[str, str]] = []
    debit_rows: list[dict[str, str]] = []
    missing: list[str] = []
    season = str(private_result.get("season", "")).strip()
    for player in players:
        _refresh_player_amounts(player)
        final_amount = _decimal_money(
            player.get("final_amount", 0),
            "Finalbetrag",
            allow_negative=True,
        )
        if final_amount == 0:
            continue
        if not _has_exportable_payment_data(player):
            missing.append(str(player.get("premium_name", "")))
            continue
        row = {
            "Name": str(player.get("premium_name", "")),
            "Kontoinhaber": str(player.get("account_holder", "")),
            "IBAN": str(player.get("iban", "")),
            "BIC": str(player.get("bic", "")),
            "Betrag": _format_money(final_amount.copy_abs()),
            "Verwendungszweck": (
                f"Spielerpraemien {season}"
                if final_amount > 0
                else f"Verrechnung Spielerpraemien {season}"
            ),
        }
        if final_amount > 0:
            transfer_rows.append(row)
        else:
            debit_rows.append(row)
    external_debit_rows, external_missing = _deckel_external_debit_rows(
        private_result,
        season,
    )
    debit_rows.extend(external_debit_rows)
    missing.extend(external_missing)

    if missing:
        raise ValueError(
            "Fuer folgende Spieler oder Deckellistenpositionen fehlen "
            "gueltige Bankdaten: "
            + ", ".join(name for name in missing if name)
        )

    result_dir = ensure_private_directory(PLAYER_PAYMENT_RESULT_DIR)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    transfer_path = result_dir / f"sammelueberweisung_{timestamp}.csv"
    debit_path = result_dir / f"sammellastschrift_{timestamp}.csv"
    _write_payment_csv(transfer_path, transfer_rows)
    _write_payment_csv(debit_path, debit_rows)
    _set_current_private_result(private_result)
    return {
        "exports": {
            "transfer": {
                "path": str(transfer_path),
                "count": len(transfer_rows),
                "total": float(
                    sum(
                        _decimal_money(row["Betrag"], "Betrag")
                        for row in transfer_rows
                    )
                ),
            },
            "debit": {
                "path": str(debit_path),
                "count": len(debit_rows),
                "total": float(
                    sum(
                        _decimal_money(row["Betrag"], "Betrag")
                        for row in debit_rows
                    )
                ),
            },
        },
        "result": _public_review(private_result),
    }


def load_deckel_list_positions(
    path: str | Path = DEFAULT_DECKEL_LIST_PATH,
) -> list[dict[str, Any]]:
    deckel_path = Path(path)
    if not deckel_path.is_file():
        raise PlayerPaymentError(f"Deckelliste nicht gefunden: {deckel_path}")
    try:
        with ZipFile(deckel_path) as workbook:
            shared_strings = _xlsx_shared_strings(workbook)
            worksheets = sorted(
                name
                for name in workbook.namelist()
                if name.startswith("xl/worksheets/sheet")
                and name.endswith(".xml")
            )
            positions: list[dict[str, Any]] = []
            for worksheet in worksheets:
                for cells in _xlsx_sheet_rows(workbook, worksheet, shared_strings):
                    position = _deckel_position_from_row(
                        cells,
                        len(positions) + 1,
                        worksheet,
                    )
                    if position is not None:
                        positions.append(position)
    except (BadZipFile, KeyError, ET.ParseError, OSError) as exc:
        raise PlayerPaymentError(
            "Deckelliste konnte nicht als XLSX gelesen werden."
        ) from exc
    if not positions:
        raise PlayerPaymentError(
            "In der Deckelliste wurden keine offenen Positionen erkannt."
        )
    return positions


def _payment_players(private_result: dict[str, Any]) -> list[dict[str, Any]]:
    players = private_result.get("players", [])
    if not isinstance(players, list):
        raise PlayerPaymentError("Zahlungsdaten-Snapshot ist ungueltig.")
    return [player for player in players if isinstance(player, dict)]


def _preview_deckel_assignments(
    positions: list[dict[str, Any]],
    players: list[dict[str, Any]],
) -> None:
    for position in positions:
        auto_assignment = _auto_assign_position(position, players)
        position.update(
            {
                "best_premium_name": auto_assignment.get("premium_name", ""),
                "match_score": auto_assignment.get("score", 0),
                "assignment_status": position.get(
                    "assignment_status",
                    "unassigned",
                ),
                "assigned_premium_name": position.get("assigned_premium_name", ""),
                "assigned_by": position.get("assigned_by", ""),
            }
        )


def _resolve_deckel_debtors(
    page: Any,
    positions: list[dict[str, Any]],
    players: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for position in positions:
        auto_assignment = _auto_assign_position(position, players)
        if auto_assignment.get("premium_name"):
            continue
        raw_name = _clean_text(position.get("raw_name", ""))
        if not raw_name:
            continue
        key = _basic_name(raw_name)
        entry = grouped.setdefault(
            key,
            {
                "premium_name": raw_name,
                "premium_total": 0,
                "teams": [],
                "deckel_debtor": True,
                "deckel_position_ids": [],
                "deckel_amount_total": 0.0,
            },
        )
        entry["deckel_position_ids"].append(str(position.get("position_id", "")))
        entry["deckel_amount_total"] = round(
            float(entry["deckel_amount_total"])
            + float(position.get("amount", 0) or 0),
            2,
        )
    debtors = []
    for debtor in grouped.values():
        resolved = _resolve_player_payment(page, debtor)
        resolved["deckel_debtor"] = True
        resolved["deckel_position_ids"] = debtor["deckel_position_ids"]
        resolved["deckel_amount_total"] = debtor["deckel_amount_total"]
        debtors.append(resolved)
    return debtors


def _apply_deckel_offsets(
    players: list[dict[str, Any]],
    positions: list[dict[str, Any]],
    assignment_payload: dict[str, Any],
) -> None:
    for position in positions:
        position_id = str(position.get("position_id", ""))
        auto_assignment = _auto_assign_position(position, players)
        override_present = position_id in assignment_payload
        requested_name = (
            _clean_text(assignment_payload.get(position_id, ""))
            if override_present
            else auto_assignment.get("premium_name", "")
        )
        player = _find_payment_player(players, requested_name)
        position.update(
            {
                "best_premium_name": auto_assignment.get("premium_name", ""),
                "match_score": auto_assignment.get("score", 0),
                "assignment_status": "unassigned",
                "assigned_premium_name": "",
                "assigned_by": "",
            }
        )
        if player is None:
            continue
        assigned_by = "manual" if override_present else "auto"
        position.update(
            {
                "assignment_status": assigned_by,
                "assigned_premium_name": str(player.get("premium_name", "")),
                "assigned_by": assigned_by,
            }
        )
        _append_offset(
            player,
            {
                "offset_id": position_id,
                "source": "deckelliste",
                "label": "Deckelliste Vereinsheim",
                "amount": position.get("amount", 0),
                "raw_name": position.get("raw_name", ""),
                "assigned_by": assigned_by,
                "classification": DECKEL_TRANSACTION_CLASSIFICATION,
            },
        )


def _apply_manual_offsets(
    players: list[dict[str, Any]],
    manual_offsets: list[Any],
) -> None:
    for index, raw_offset in enumerate(manual_offsets, start=1):
        if not isinstance(raw_offset, dict):
            raise ValueError("Manuelle Gegenposition muss ein Objekt sein.")
        premium_name = _manual_text(
            raw_offset.get("premium_name"),
            "Spieler",
            200,
        )
        player = _find_payment_player(players, premium_name)
        if player is None:
            raise LookupError(
                f"Spieler fuer manuelle Gegenposition nicht gefunden: {premium_name}"
            )
        amount = _positive_money(raw_offset.get("amount"), "Betrag")
        label = _clean_text(raw_offset.get("label", ""))
        if not label:
            label = "Manuelle Gegenposition"
        if len(label) > 200:
            raise ValueError("Bezeichnung der Gegenposition ist zu lang.")
        _append_offset(
            player,
            {
                "offset_id": "manual_"
                + _stable_hash(f"{index}|{premium_name}|{label}|{amount}"),
                "source": "manual",
                "label": label,
                "amount": amount,
                "raw_name": premium_name,
                "assigned_by": "manual",
                "classification": _classification_payload(
                    raw_offset.get("classification"),
                    {},
                ),
            },
        )


def _find_payment_player(
    players: list[dict[str, Any]],
    premium_name: str,
) -> dict[str, Any] | None:
    normalized = _clean_text(premium_name).casefold()
    if not normalized:
        return None
    for player in players:
        if _clean_text(player.get("premium_name", "")).casefold() == normalized:
            return player
    return None


def _auto_assign_position(
    position: dict[str, Any],
    players: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_name = str(position.get("raw_name", ""))
    scored = sorted(
        (
            (
                _name_similarity_text(raw_name, str(player.get("premium_name", ""))),
                str(player.get("premium_name", "")),
            )
            for player in players
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    if not scored:
        return {"premium_name": "", "score": 0}
    top_score, top_name = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0
    if (
        top_score >= OFFSET_MATCH_THRESHOLD
        and top_score - second_score >= OFFSET_AMBIGUITY_MARGIN
    ):
        return {"premium_name": top_name, "score": round(top_score, 3)}
    return {"premium_name": "", "score": round(top_score, 3)}


def _append_offset(player: dict[str, Any], raw_offset: dict[str, Any]) -> None:
    offsets = player.setdefault("offsets", [])
    if not isinstance(offsets, list):
        offsets = []
        player["offsets"] = offsets
    offsets.append(_normalize_offset(raw_offset))


def _refresh_player_amounts(player: dict[str, Any]) -> None:
    premium_total = _decimal_money(
        player.get("premium_total", 0),
        "Praemie",
        allow_negative=False,
    )
    offsets = [
        _normalize_offset(offset)
        for offset in player.get("offsets", [])
        if isinstance(offset, dict)
    ]
    offset_total = sum(
        (_decimal_money(offset.get("amount", 0), "Betrag") for offset in offsets),
        Decimal("0.00"),
    ).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    final_amount = (premium_total - offset_total).quantize(
        MONEY_QUANT,
        rounding=ROUND_HALF_UP,
    )
    player["offsets"] = offsets
    player["offset_total"] = float(offset_total)
    player["final_amount"] = float(final_amount)
    player["payment_direction"] = (
        "transfer"
        if final_amount > 0
        else "debit"
        if final_amount < 0
        else "balanced"
    )
    player["transaction_splits"] = _transaction_splits(premium_total, offsets)


def _normalize_offset(raw_offset: dict[str, Any]) -> dict[str, Any]:
    amount = _positive_money(raw_offset.get("amount"), "Betrag")
    offset_id = _clean_text(raw_offset.get("offset_id", ""))
    if not offset_id:
        offset_id = "offset_" + _stable_hash(
            "|".join(
                (
                    str(raw_offset.get("source", "")),
                    str(raw_offset.get("label", "")),
                    str(amount),
                    str(raw_offset.get("raw_name", "")),
                )
            )
        )
    return {
        "offset_id": offset_id,
        "source": _clean_text(raw_offset.get("source", "manual")) or "manual",
        "label": _clean_text(raw_offset.get("label", "Gegenposition")),
        "amount": float(amount),
        "raw_name": _clean_text(raw_offset.get("raw_name", "")),
        "assigned_by": _clean_text(raw_offset.get("assigned_by", "")),
        "classification": _classification_payload(
            raw_offset.get("classification"),
            {},
        ),
    }


def _transaction_splits(
    premium_total: Decimal,
    offsets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    splits = [
        {
            "label": "Spielerpraemien",
            "amount": float(premium_total),
            "direction": "premium",
            "classification": dict(PREMIUM_TRANSACTION_CLASSIFICATION),
        }
    ]
    for offset in offsets:
        amount = _decimal_money(offset.get("amount", 0), "Betrag")
        splits.append(
            {
                "label": offset.get("label", "Gegenposition"),
                "amount": float(-amount),
                "direction": "offset",
                "source": offset.get("source", ""),
                "classification": _classification_payload(
                    offset.get("classification"),
                    {},
                ),
            }
        )
    return splits


def _classification_payload(
    value: Any,
    default: dict[str, str],
) -> dict[str, str]:
    result = dict(default)
    if not isinstance(value, dict):
        return result
    for key in ("transaction_type", "top_category", "sub_category", "sphere"):
        text = _clean_text(value.get(key, ""))
        if len(text) > 120:
            raise ValueError("Klassifizierungsangabe ist zu lang.")
        if text:
            result[key] = text
        elif key not in result:
            result[key] = ""
    return result


def _xlsx_shared_strings(workbook: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return []
    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    values = []
    for item in root.findall(".//main:si", XLSX_NS):
        pieces = [
            node.text or ""
            for node in item.iter()
            if str(node.tag).endswith("}t")
        ]
        values.append("".join(pieces))
    return values


def _xlsx_sheet_rows(
    workbook: ZipFile,
    worksheet: str,
    shared_strings: list[str],
) -> Iterable[list[str]]:
    root = ET.fromstring(workbook.read(worksheet))
    for row in root.findall(".//main:sheetData/main:row", XLSX_NS):
        yield [
            _xlsx_cell_value(cell, shared_strings)
            for cell in row.findall("main:c", XLSX_NS)
        ]


def _xlsx_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(
            node.text or ""
            for node in cell.findall(".//main:t", XLSX_NS)
        )
    value_node = cell.find("main:v", XLSX_NS)
    if value_node is None:
        return ""
    value = value_node.text or ""
    if cell_type == "s":
        try:
            return shared_strings[int(value)]
        except (ValueError, IndexError):
            return ""
    return value


def _deckel_position_from_row(
    cells: list[str],
    sequence: int,
    worksheet: str,
) -> dict[str, Any] | None:
    cleaned = [_clean_text(value) for value in cells]
    non_empty = [value for value in cleaned if value]
    if not non_empty:
        return None
    name = next(
        (
            value
            for value in non_empty
            if _try_decimal_money(value) is None
            and not _looks_like_deckel_header(value)
        ),
        "",
    )
    if not name or _looks_like_deckel_header(name):
        return None
    amount_candidates = [
        amount
        for amount in (_try_positive_money(value) for value in cleaned[1:])
        if amount is not None and amount > 0
    ]
    if not amount_candidates:
        return None
    amount = amount_candidates[-1]
    position_id = "deckel_" + _stable_hash(
        f"{worksheet}|{sequence}|{name}|{amount}"
    )
    return {
        "position_id": position_id,
        "source": "deckelliste",
        "raw_name": name,
        "amount": float(amount),
        "label": "Deckelliste Vereinsheim",
        "assignment_status": "unassigned",
        "assigned_premium_name": "",
        "assigned_by": "",
        "match_score": 0,
        "classification": dict(DECKEL_TRANSACTION_CLASSIFICATION),
    }


def _looks_like_deckel_header(value: str) -> bool:
    normalized = _basic_name(value)
    return normalized in {
        "name",
        "spieler",
        "mitglied",
        "person",
        "gesamt",
        "gesamtbetrag",
        "summe",
        "betrag",
    } or normalized.startswith("gesamt ")


def _has_exportable_payment_data(player: dict[str, Any]) -> bool:
    validation = player.get("validation", {})
    iban = validation.get("iban", {}) if isinstance(validation, dict) else {}
    bic = validation.get("bic", {}) if isinstance(validation, dict) else {}
    return bool(
        player.get("iban")
        and player.get("bic")
        and iban.get("valid")
        and bic.get("valid")
    )


def _write_payment_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["Name", "Kontoinhaber", "IBAN", "BIC", "Betrag", "Verwendungszweck"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    protect_file(path)


def _deckel_external_debit_rows(
    private_result: dict[str, Any],
    season: str,
) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    missing: list[str] = []
    for debtor, amount, label in _deckel_external_debit_candidates(private_result):
        if not _has_exportable_payment_data(debtor):
            missing.append(label)
            continue
        rows.append(
            {
                "Name": label,
                "Kontoinhaber": str(debtor.get("account_holder", "")),
                "IBAN": str(debtor.get("iban", "")),
                "BIC": str(debtor.get("bic", "")),
                "Betrag": _format_money(amount),
                "Verwendungszweck": f"Deckelliste Vereinsheim {season}",
            }
        )
    return rows, missing


def _deckel_external_debit_candidates(
    private_result: dict[str, Any],
) -> list[tuple[dict[str, Any], Decimal, str]]:
    configuration = private_result.get("offset_configuration", {})
    positions = (
        configuration.get("deckel_positions", [])
        if isinstance(configuration, dict)
        else []
    )
    unassigned_amounts: dict[str, Decimal] = {}
    unassigned_labels: dict[str, str] = {}
    for position in positions:
        if not isinstance(position, dict):
            continue
        if position.get("assignment_status") != "unassigned":
            continue
        position_id = str(position.get("position_id", ""))
        if not position_id:
            continue
        amount = _decimal_money(position.get("amount", 0), "Betrag")
        unassigned_amounts[position_id] = amount
        unassigned_labels[position_id] = _clean_text(
            position.get("raw_name", "")
        ) or "Deckelliste"
    candidates = []
    for debtor in private_result.get("deckel_debtors", []):
        if not isinstance(debtor, dict):
            continue
        ids = [
            str(value)
            for value in debtor.get("deckel_position_ids", [])
            if str(value) in unassigned_amounts
        ]
        if not ids:
            continue
        amount = sum(
            (unassigned_amounts[position_id] for position_id in ids),
            Decimal("0.00"),
        ).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
        if amount <= 0:
            continue
        labels = list(dict.fromkeys(unassigned_labels[position_id] for position_id in ids))
        candidates.append((debtor, amount, ", ".join(labels)))
    return candidates


def _format_money(value: Decimal) -> str:
    return f"{value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP):.2f}".replace(
        ".",
        ",",
    )


def _positive_money(value: Any, label: str) -> Decimal:
    amount = _decimal_money(value, label, allow_negative=True).copy_abs()
    if amount <= 0:
        raise ValueError(f"{label} muss groesser als 0 sein.")
    return amount


def _try_positive_money(value: Any) -> Decimal | None:
    try:
        return _positive_money(value, "Betrag")
    except ValueError:
        return None


def _try_decimal_money(value: Any) -> Decimal | None:
    try:
        return _decimal_money(value, "Betrag", allow_negative=True)
    except ValueError:
        return None


def _decimal_money(
    value: Any,
    label: str,
    *,
    allow_negative: bool = False,
) -> Decimal:
    if isinstance(value, Decimal):
        amount = value
    elif isinstance(value, int):
        amount = Decimal(value)
    elif isinstance(value, float):
        amount = Decimal(str(value))
    else:
        text = _clean_text(value)
        if not text:
            raise ValueError(f"{label} fehlt.")
        text = text.replace("\u00a0", " ").replace("'", "")
        text = re.sub(r"\s+", "", text)
        if "," in text and "." in text:
            if text.rfind(",") > text.rfind("."):
                text = text.replace(".", "").replace(",", ".")
            else:
                text = text.replace(",", "")
        elif "," in text:
            text = text.replace(",", ".")
        text = re.sub(r"[^0-9.+-]", "", text)
        if text in {"", ".", "-", "+", "+.", "-."}:
            raise ValueError(f"{label} ist kein gueltiger Betrag.")
        try:
            amount = Decimal(text)
        except InvalidOperation as exc:
            raise ValueError(f"{label} ist kein gueltiger Betrag.") from exc
    if not amount.is_finite():
        raise ValueError(f"{label} ist kein gueltiger Betrag.")
    amount = amount.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    if amount < 0 and not allow_negative:
        raise ValueError(f"{label} darf nicht negativ sein.")
    return amount


def _name_similarity_text(left: str, right: str) -> float:
    if _basic_name(left) == _basic_name(right):
        return 1.0
    scores = []
    for expand_umlauts in (True, False):
        left_tokens = _name_tokens(left, expand_umlauts)
        right_tokens = _name_tokens(right, expand_umlauts)
        if not left_tokens or not right_tokens:
            continue
        if sorted(left_tokens) == sorted(right_tokens):
            return 1.0
        scores.append(
            SequenceMatcher(
                None,
                " ".join(left_tokens),
                " ".join(right_tokens),
            ).ratio()
        )
        scores.append(
            SequenceMatcher(
                None,
                " ".join(sorted(left_tokens)),
                " ".join(sorted(right_tokens)),
            ).ratio()
        )
    return max(scores, default=0.0)


def _stable_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:12]


def _resolve_player_payment(
    page: Any,
    player: dict[str, Any],
) -> dict[str, Any]:
    premium_name = str(player["premium_name"])
    candidates: dict[str, MemberCandidate] = {}
    match = _match_result("kein_treffer", "nicht_gefunden", 0.0, None)
    _open_members(page)
    page.wait_for_timeout(700)
    for query in _member_search_queries(premium_name):
        for candidate in _search_members(page, query):
            candidates[candidate.member_id] = candidate
        match = match_member_name(premium_name, candidates.values())
        if (
            match["status"] == "eindeutig_gefunden"
            and match["quality"] in {"exakt", "normalisiert"}
        ):
            break

    base = {
        **player,
        "member_id": "",
        "member_name": match["member_name"],
        "match_quality": match["quality"],
        "match_score": match["score"],
        "status": match["status"],
        "candidate_count": match["candidate_count"],
        "payment_source": "none",
        "account_holder": "",
        "iban": "",
        "bic": "",
        "validation": validate_payment_data("", ""),
        "manual_confirmation_required": True,
        "approved_for_sepa": False,
    }
    candidate = match.get("candidate")
    if (
        match["status"] != "eindeutig_gefunden"
        or match["quality"] not in {"exakt", "normalisiert"}
        or not isinstance(candidate, MemberCandidate)
    ):
        return base

    payment = _read_payment_data(page, candidate)
    validation = validate_payment_data(payment["iban"], payment["bic"])
    status = (
        "eindeutig_gefunden"
        if validation["valid_for_manual_confirmation"]
        else "manuell_pruefen"
    )
    return {
        **base,
        "member_id": candidate.member_id,
        "member_name": candidate.display_name,
        "status": status,
        "payment_source": "dfbnet",
        "account_holder": payment["account_holder"],
        "iban": validation["iban"]["normalized"],
        "bic": validation["bic"]["normalized"],
        "validation": validation,
    }


def _search_members(page: Any, query: str) -> list[MemberCandidate]:
    search = page.locator("input[name='searchAll']")
    if not search.count():
        raise PlayerPaymentError("Die DFBnet-Mitgliedersuche wurde nicht gefunden.")
    search.first.click()
    search.first.fill(query)
    search_button = page.locator(
        "form[name='FormSearchAll'] img[alt='Suchen']"
    )
    if not search_button.count():
        raise PlayerPaymentError("Die DFBnet-Suchschaltfläche wurde nicht gefunden.")
    search_button.first.click()
    page.wait_for_load_state("domcontentloaded", timeout=60_000)
    page.locator("input[name='searchAll']").wait_for(
        state="attached",
        timeout=30_000,
    )
    page.wait_for_timeout(1_000)
    result: dict[str, MemberCandidate] = {}
    while True:
        for candidate in _member_candidates_on_page(page):
            result[candidate.member_id] = candidate
        current_page, total_pages = _search_page_numbers(page)
        if current_page >= total_pages:
            break
        next_button = page.locator("input[name='Next1']").filter(visible=True)
        if not next_button.count():
            break
        next_button.first.click()
        page.wait_for_load_state("domcontentloaded", timeout=60_000)
        page.locator("input[name='searchAll']").wait_for(
            state="attached",
            timeout=30_000,
        )
        page.wait_for_timeout(700)
    return list(result.values())


def _member_candidates_on_page(page: Any) -> list[MemberCandidate]:
    result = []
    checkboxes = page.locator("input[name^='ChkToDelAdress']")
    for index in range(checkboxes.count()):
        checkbox = checkboxes.nth(index)
        row = checkbox.locator("xpath=ancestor::tr[1]")
        cells = row.locator("td")
        if cells.count() < 5:
            continue
        member_id = _clean_text(checkbox.input_value())
        surname = _clean_text(cells.nth(3).inner_text())
        first_name = _clean_text(cells.nth(4).inner_text())
        link = cells.nth(3).locator("a")
        detail_url = _detail_url(link.first.get_attribute("href") if link.count() else "")
        if member_id and surname and first_name and detail_url:
            result.append(
                MemberCandidate(
                    member_id=member_id,
                    surname=surname,
                    first_name=first_name,
                    detail_url=detail_url,
                )
            )
    return result


def _read_payment_data(
    page: Any,
    candidate: MemberCandidate,
) -> dict[str, str]:
    page.goto(candidate.detail_url, wait_until="domcontentloaded", timeout=60_000)
    page.locator("#TabButtons").wait_for(state="attached", timeout=30_000)
    page.wait_for_timeout(500)
    payment_tab = page.locator("#TabButtons a").filter(
        has_text=re.compile(r"^\s*Zahlungsdaten\s*$", re.IGNORECASE)
    )
    if not payment_tab.count():
        raise PlayerPaymentError(
            "Der Reiter Zahlungsdaten wurde im Mitglied nicht gefunden."
        )
    payment_url = payment_tab.first.get_attribute("href") or ""
    if not payment_url.startswith("https://verein.dfbnet.org/"):
        raise PlayerPaymentError("Der Zahlungsdaten-Link ist ungültig.")
    payment_tab.first.click()
    page.wait_for_load_state("domcontentloaded", timeout=60_000)
    page.locator("#strIban").wait_for(
        state="attached",
        timeout=30_000,
    )
    page.wait_for_timeout(300)
    iban = page.locator("#strIban")
    bic = page.locator("#strBic")
    holder = page.locator("#strKontoinhaber")
    if not iban.count() or not bic.count() or not holder.count():
        raise PlayerPaymentError(
            "Die Zahlungsdatenfelder wurden im Mitglied nicht gefunden."
        )
    return {
        "account_holder": _clean_text(holder.first.input_value()),
        "iban": iban.first.input_value(),
        "bic": bic.first.input_value(),
    }


def _open_members(page: Any) -> str:
    links = page.locator("#mgmenu1 a")
    for index in range(links.count()):
        link = links.nth(index)
        if _clean_text(link.inner_text()) != "Mitglieder":
            continue
        href = link.get_attribute("href") or ""
        if href.startswith("https://verein.dfbnet.org/"):
            page.goto(href, wait_until="domcontentloaded", timeout=60_000)
            page.locator("input[name='searchAll']").wait_for(
                state="attached",
                timeout=30_000,
            )
            page.wait_for_timeout(500)
            if page.locator("input[name='searchAll']").count():
                return href
    raise PlayerPaymentError("Die DFBnet-Mitgliederverwaltung wurde nicht gefunden.")


def _login(page: Any, username: str, password: str) -> None:
    page.goto(
        DFBNET_VEREIN_LOGIN_URL,
        wait_until="domcontentloaded",
        timeout=60_000,
    )
    username_input = page.locator("input[name='strUserName']")
    password_input = page.locator("input[name='strPass']")
    if username_input.count() and password_input.count():
        username_input.first.fill(username)
        password_input.first.fill(password)
        submit = page.locator("#anmelden")
        if not submit.count():
            raise PlayerPaymentError(
                "Die DFBnet-Verein-Anmeldeschaltfläche wurde nicht gefunden."
            )
        submit.first.click()
        page.wait_for_load_state("domcontentloaded", timeout=60_000)
    try:
        page.locator("#mgmenu1").wait_for(state="attached", timeout=30_000)
        page.wait_for_timeout(1_000)
    except Exception as exc:
        raise PlayerPaymentError(
            "Der Login bei DFBnet Verein konnte nicht bestätigt werden."
        ) from exc


def _load_credentials() -> tuple[str, str]:
    try:
        from dotenv import dotenv_values
    except ModuleNotFoundError as exc:
        raise PlayerPaymentError(
            "python-dotenv fehlt. Abhängigkeiten aus requirements.txt installieren."
        ) from exc
    if not SECRETS_PATH.is_file():
        raise PlayerPaymentError(f"Secrets-Datei fehlt: {SECRETS_PATH}")
    values = dotenv_values(
        SECRETS_PATH,
        encoding="utf-8-sig",
        interpolate=False,
    )
    username = values.get("DFBNETVEREIN_USERNAME")
    password = values.get("DFBNETVEREIN_PASSWORD")
    if not isinstance(username, str) or not username:
        raise PlayerPaymentError(
            "Credential-Variable 'DFBNETVEREIN_USERNAME' fehlt oder ist leer."
        )
    if not isinstance(password, str) or not password:
        raise PlayerPaymentError(
            "Credential-Variable 'DFBNETVEREIN_PASSWORD' fehlt oder ist leer."
        )
    return username, password


def _set_current_private_result(result: dict[str, Any]) -> None:
    global _CURRENT_PRIVATE_RESULT
    with _PAYMENT_SESSION_LOCK:
        _CURRENT_PRIVATE_RESULT = copy.deepcopy(result)


def _get_current_private_result() -> dict[str, Any] | None:
    with _PAYMENT_SESSION_LOCK:
        return (
            copy.deepcopy(_CURRENT_PRIVATE_RESULT)
            if _CURRENT_PRIVATE_RESULT is not None
            else None
        )


def _apply_manual_override(
    player: dict[str, Any],
    override: dict[str, Any],
) -> None:
    validation = override.get("validation")
    if not isinstance(validation, dict):
        validation = validate_payment_data(
            str(override.get("iban", "")),
            str(override.get("bic", "")),
        )
    player.update(
        {
            "account_holder": str(override.get("account_holder", "")),
            "iban": str(
                validation.get("iban", {}).get("normalized", "")
            ),
            "bic": str(
                validation.get("bic", {}).get("normalized", "")
            ),
            "validation": validation,
            "payment_source": "manual",
            "status": "manuell_pruefen",
            "manual_payment_updated_at": override.get("updated_at", ""),
            "manual_confirmation_required": True,
            "approved_for_sepa": False,
        }
    )


def _manual_text(value: Any, label: str, maximum_length: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} muss als Text angegeben werden.")
    normalized = _clean_text(value)
    if not normalized:
        raise ValueError(f"{label} fehlt.")
    if len(normalized) > maximum_length:
        raise ValueError(f"{label} ist zu lang.")
    return normalized


def _premium_team_definitions(
    premium_result: dict[str, Any],
) -> list[dict[str, str]]:
    return [
        {
            "team_id": str(team.get("team_id", "")).strip(),
            "label": str(team.get("label", "")).strip(),
        }
        for team in premium_result.get("teams", [])
        if isinstance(team, dict) and str(team.get("team_id", "")).strip()
    ]


def _public_review(private_result: dict[str, Any]) -> dict[str, Any]:
    rows = []
    counts = {
        "eindeutig_gefunden": 0,
        "manuell_pruefen": 0,
        "nicht_gefunden": 0,
    }
    totals = {
        "premium_total": Decimal("0.00"),
        "offset_total": Decimal("0.00"),
        "transfer_total": Decimal("0.00"),
        "debit_total": Decimal("0.00"),
        "deckel_external_debit_total": Decimal("0.00"),
        "balanced_count": 0,
    }
    for item in private_result.get("players", []):
        if not isinstance(item, dict):
            continue
        _refresh_player_amounts(item)
        status = item.get("status", "nicht_gefunden")
        counts[status] = counts.get(status, 0) + 1
        validation = item.get("validation", {})
        iban_result = validation.get("iban", {})
        bic_result = validation.get("bic", {})
        premium_total = _decimal_money(
            item.get("premium_total", 0),
            "Praemie",
            allow_negative=False,
        )
        offset_total = _decimal_money(
            item.get("offset_total", 0),
            "Verrechnung",
            allow_negative=False,
        )
        final_amount = _decimal_money(
            item.get("final_amount", 0),
            "Finalbetrag",
            allow_negative=True,
        )
        totals["premium_total"] += premium_total
        totals["offset_total"] += offset_total
        if final_amount > 0:
            totals["transfer_total"] += final_amount
        elif final_amount < 0:
            totals["debit_total"] += final_amount.copy_abs()
        else:
            totals["balanced_count"] += 1
        rows.append(
            {
                "premium_name": item.get("premium_name", ""),
                "premium_total": float(premium_total),
                "teams": item.get("teams", []),
                "member_name": item.get("member_name", ""),
                "match_quality": item.get("match_quality", "kein_treffer"),
                "match_score": item.get("match_score", 0),
                "status": status,
                "candidate_count": item.get("candidate_count", 0),
                "payment_source": item.get("payment_source", "none"),
                "masked_iban": mask_iban(iban_result.get("normalized", "")),
                "bic": bic_result.get("normalized", ""),
                "iban_valid": bool(iban_result.get("valid")),
                "bic_valid": bool(bic_result.get("valid")),
                "iban_bic_assignment": validation.get(
                    "iban_bic_assignment",
                    "nicht_geprueft",
                ),
                "manual_confirmation_required": True,
                "approved_for_sepa": False,
                "offsets": item.get("offsets", []),
                "offset_total": float(offset_total),
                "final_amount": float(final_amount),
                "payment_direction": item.get("payment_direction", "balanced"),
                "transaction_splits": item.get("transaction_splits", []),
            }
        )
    deckel_debtors = _public_deckel_debtors(private_result)
    for debtor, amount, _label in _deckel_external_debit_candidates(private_result):
        totals["deckel_external_debit_total"] += amount
        totals["debit_total"] += amount
    teams = [
        {
            "team_id": str(team.get("team_id", "")),
            "label": str(team.get("label", "")),
        }
        for team in private_result.get("teams", [])
        if isinstance(team, dict)
    ]
    return {
        "season": private_result.get("season", ""),
        "generated_at": private_result.get("generated_at", ""),
        "premium_generated_at": private_result.get("premium_generated_at", ""),
        "players": rows,
        "teams": teams,
        "team_groups": _public_team_groups(rows, teams),
        "counts": counts,
        "warnings": private_result.get("warnings", []),
        "totals": {
            key: (
                float(value)
                if isinstance(value, Decimal)
                else value
            )
            for key, value in totals.items()
        },
        "offset_configuration": _public_offset_configuration(
            private_result.get("offset_configuration", {}),
            deckel_debtors,
        ),
        "deckel_debtors": deckel_debtors,
        "default_deckel_path": str(DEFAULT_DECKEL_LIST_PATH),
        "manual_confirmation_required": True,
    }


def _public_deckel_debtors(private_result: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for debtor in private_result.get("deckel_debtors", []):
        if not isinstance(debtor, dict):
            continue
        validation = debtor.get("validation", {})
        iban_result = validation.get("iban", {}) if isinstance(validation, dict) else {}
        bic_result = validation.get("bic", {}) if isinstance(validation, dict) else {}
        result.append(
            {
                "premium_name": debtor.get("premium_name", ""),
                "deckel_position_ids": debtor.get("deckel_position_ids", []),
                "deckel_amount_total": debtor.get("deckel_amount_total", 0),
                "member_name": debtor.get("member_name", ""),
                "match_quality": debtor.get("match_quality", "kein_treffer"),
                "match_score": debtor.get("match_score", 0),
                "status": debtor.get("status", "nicht_gefunden"),
                "payment_source": debtor.get("payment_source", "none"),
                "masked_iban": mask_iban(iban_result.get("normalized", "")),
                "bic": bic_result.get("normalized", ""),
                "iban_valid": bool(iban_result.get("valid")),
                "bic_valid": bool(bic_result.get("valid")),
            }
        )
    return result


def _public_offset_configuration(
    value: Any,
    deckel_debtors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {
            "deckel_path": "",
            "deckel_positions": [],
            "updated_at": "",
        }
    debtor_by_position: dict[str, dict[str, Any]] = {}
    for debtor in deckel_debtors or []:
        for position_id in debtor.get("deckel_position_ids", []):
            debtor_by_position[str(position_id)] = debtor
    positions = []
    for position in value.get("deckel_positions", []):
        if not isinstance(position, dict):
            continue
        position_id = str(position.get("position_id", ""))
        debtor = debtor_by_position.get(position_id, {})
        positions.append(
            {
                "position_id": position_id,
                "source": position.get("source", "deckelliste"),
                "raw_name": position.get("raw_name", ""),
                "amount": position.get("amount", 0),
                "label": position.get("label", ""),
                "assignment_status": position.get(
                    "assignment_status",
                    "unassigned",
                ),
                "assigned_premium_name": position.get(
                    "assigned_premium_name",
                    "",
                ),
                "best_premium_name": position.get("best_premium_name", ""),
                "match_score": position.get("match_score", 0),
                "classification": position.get(
                    "classification",
                    dict(DECKEL_TRANSACTION_CLASSIFICATION),
                ),
                "external_debtor": debtor,
            }
        )
    return {
        "deckel_path": value.get("deckel_path", ""),
        "deckel_positions": positions,
        "updated_at": value.get("updated_at", ""),
    }


def _public_team_groups(
    rows: list[dict[str, Any]],
    teams: list[dict[str, str]],
) -> list[dict[str, Any]]:
    groups = [
        {
            "team_id": team["team_id"],
            "label": team["label"],
            "players": [],
        }
        for team in teams
    ]
    by_id = {group["team_id"]: group for group in groups}
    for row in rows:
        allocations = row.get("teams", [])
        for allocation in allocations:
            if not isinstance(allocation, dict):
                continue
            team_id = str(allocation.get("team_id", ""))
            group = by_id.get(team_id)
            if group is None:
                group = {
                    "team_id": team_id,
                    "label": str(allocation.get("label", team_id)),
                    "players": [],
                }
                groups.append(group)
                by_id[team_id] = group
            team_row = dict(row)
            team_row["combined_premium_total"] = row.get("premium_total", 0)
            team_row["premium_total"] = allocation.get(
                "premium_total",
                row.get("premium_total", 0),
            )
            group["players"].append(team_row)
    return groups


def _member_search_queries(value: str) -> list[str]:
    original_tokens = re.findall(
        r"[^\W\d_]+(?:[-'’][^\W\d_]+)*",
        _clean_text(value),
        flags=re.UNICODE,
    )
    normalized_tokens = _name_tokens(value, expand_umlauts=True)
    simplified_tokens = _name_tokens(value, expand_umlauts=False)
    queries = []
    for token in sorted(original_tokens, key=len, reverse=True):
        if len(token) >= 3:
            queries.append(token)
    queries.append(_clean_text(value))
    for token in sorted(
        {*normalized_tokens, *simplified_tokens},
        key=len,
        reverse=True,
    ):
        if len(token) >= 3:
            queries.append(token)
    if len(original_tokens) >= 2:
        queries.append(" ".join(reversed(original_tokens)))
    return list(dict.fromkeys(query for query in queries if query))[:8]


def _is_exact_name_match(
    premium_name: str,
    candidate: MemberCandidate,
) -> bool:
    premium = _basic_name(premium_name)
    return premium in {
        _basic_name(candidate.display_name),
        _basic_name(candidate.source_order_name),
    }


def _is_normalized_name_match(
    premium_name: str,
    candidate: MemberCandidate,
) -> bool:
    for expand_umlauts in (True, False):
        premium = sorted(_name_tokens(premium_name, expand_umlauts))
        member = sorted(_name_tokens(candidate.display_name, expand_umlauts))
        if premium and premium == member:
            return True
    return False


def _name_similarity(
    premium_name: str,
    candidate: MemberCandidate,
) -> float:
    scores = []
    for expand_umlauts in (True, False):
        premium_tokens = _name_tokens(premium_name, expand_umlauts)
        if not premium_tokens:
            continue
        for member_name in (
            candidate.display_name,
            candidate.source_order_name,
        ):
            member_tokens = _name_tokens(member_name, expand_umlauts)
            scores.append(
                SequenceMatcher(
                    None,
                    " ".join(premium_tokens),
                    " ".join(member_tokens),
                ).ratio()
            )
            scores.append(
                SequenceMatcher(
                    None,
                    " ".join(sorted(premium_tokens)),
                    " ".join(sorted(member_tokens)),
                ).ratio()
            )
    return max(scores, default=0.0)


def _name_tokens(value: str, expand_umlauts: bool) -> list[str]:
    text = _clean_text(value).casefold()
    replacements = (
        {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
        if expand_umlauts
        else {"ä": "a", "ö": "o", "ü": "u", "ß": "ss"}
    )
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = re.sub(r"[-‐‑‒–—'’.,/]+", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return [token for token in text.split() if token]


def _basic_name(value: str) -> str:
    text = _clean_text(value).casefold()
    text = re.sub(r"[,]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _match_result(
    quality: str,
    status: str,
    score: float,
    candidate: MemberCandidate | None,
    candidates: Iterable[MemberCandidate] = (),
) -> dict[str, Any]:
    candidate_list = list(candidates)
    if candidate is not None and not candidate_list:
        candidate_list = [candidate]
    return {
        "quality": quality,
        "status": status,
        "score": round(float(score), 3),
        "candidate": candidate,
        "member_name": candidate.display_name if candidate is not None else "",
        "candidate_count": len(candidate_list),
    }


def _iban_mod97(value: str) -> int:
    rearranged = value[4:] + value[:4]
    remainder = 0
    for character in rearranged:
        digits = (
            str(ord(character) - ord("A") + 10)
            if character.isalpha()
            else character
        )
        for digit in digits:
            remainder = (remainder * 10 + int(digit)) % 97
    return remainder


def _search_page_numbers(page: Any) -> tuple[int, int]:
    match = re.search(
        r"Seite\s+(\d+)\s+von\s+(\d+)",
        page.locator("body").inner_text(),
        re.IGNORECASE,
    )
    return (
        (int(match.group(1)), int(match.group(2)))
        if match
        else (1, 1)
    )


def _detail_url(value: str | None) -> str:
    href = str(value or "")
    if href.startswith("https://verein.dfbnet.org/"):
        return href
    match = re.search(r"OnSubmitUrl\('([^']+)'\)", href)
    if match and match.group(1).startswith("https://verein.dfbnet.org/"):
        return match.group(1)
    return ""


def _fresh_page(context: Any) -> Any:
    page = context.new_page()
    for existing in list(context.pages):
        if existing is page or existing.is_closed():
            continue
        existing.close()
    return page


def _clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _save_error_screenshot(page: Any | None, logger: logging.Logger) -> None:
    if page is None or page.is_closed():
        return
    try:
        screenshot_dir = ensure_private_directory(
            PROJECT_ROOT / ".runtime" / "screenshots"
        )
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        path = screenshot_dir / f"dfbnet_verein_payment_{timestamp}.png"
        page.screenshot(
            path=str(path),
            full_page=False,
            mask=[
                page.locator("input"),
                page.locator("textarea"),
                page.locator("select"),
                page.locator("table"),
            ],
            mask_color="#000000",
        )
        protect_file(path)
    except Exception as exc:
        logger.warning(
            "DFBnet-Verein-Fehler-Screenshot fehlgeschlagen: %s",
            type(exc).__name__,
        )
