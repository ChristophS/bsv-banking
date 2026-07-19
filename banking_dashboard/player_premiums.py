from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urljoin

from banking_readonly.security import ensure_private_directory, protect_file


DFBNET_LOGIN_URL = "https://www.dfbnet.org/spielplus/login.do"
DFBNET_MATCH_REPORT_URL = (
    "https://www.dfbnet.org/spielplus/mod_sbo/webflow.do"
    "?event=START&dmg_menu=102"
)
SECRETS_PATH = Path("D:/.secrets/bsv_banking.env")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DFBNET_PROFILE_DIR = PROJECT_ROOT / ".runtime" / "session" / "dfbnet-chromium"
DFBNET_RESULT_DIR = PROJECT_ROOT / ".runtime" / "dfbnet" / "player_premiums"
MIN_SEASON_START_YEAR = 2022
DFBNET_CLUB_NAME = "BSV Viktoria Bielstein 1920 e.V."


@dataclass(frozen=True)
class TeamDefinition:
    team_id: str
    label: str
    dfbnet_name: str
    default_point_value: float


TEAMS = (
    TeamDefinition(
        "herren_1",
        "BSV - Herren 1",
        "BSV Viktoria Bielstein 1920 e.V.",
        5.0,
    ),
    TeamDefinition(
        "herren_2",
        "BSV - Herren 2",
        "BSV Viktoria Bielstein 1920 e.V. II",
        2.5,
    ),
    TeamDefinition(
        "damen",
        "BSV - Damen",
        "BSV Viktoria Bielstein 1920 e.V. Frauen",
        2.5,
    ),
)
TEAM_BY_ID = {team.team_id: team for team in TEAMS}


class PlayerPremiumError(RuntimeError):
    pass


@dataclass(frozen=True)
class MatchSummary:
    match_id: str
    label: str
    date: str
    competition: str
    competition_type: str
    round: str
    opponent: str
    result: str
    outcome: str
    points: int
    detail_href: str
    row_text: str
    home_team: str = ""
    away_team: str = ""
    is_home: bool = False


def available_seasons(today: date | None = None) -> list[str]:
    current = today or date.today()
    current_start = current.year if current.month >= 7 else current.year - 1
    return [
        f"{year}/{year + 1}"
        for year in range(current_start, MIN_SEASON_START_YEAR - 1, -1)
    ]


def season_date_range(season: str) -> tuple[date, date]:
    match = re.fullmatch(r"(\d{4})/(\d{4})", str(season).strip())
    if not match:
        raise ValueError("Saison muss das Format XXXX/YYYY haben.")
    start_year, end_year = (int(value) for value in match.groups())
    if start_year < MIN_SEASON_START_YEAR or end_year != start_year + 1:
        raise ValueError(
            "Saison muss ab 2022 beginnen und zwei aufeinanderfolgende "
            "Jahre enthalten."
        )
    return date(start_year, 7, 1), date(end_year, 6, 30)


def validate_team_ids(team_ids: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(dict.fromkeys(str(value).strip() for value in team_ids))
    if not normalized:
        raise ValueError("Mindestens eine Mannschaft muss ausgewählt werden.")
    unknown = sorted(set(normalized) - set(TEAM_BY_ID))
    if unknown:
        raise ValueError(f"Unbekannte Mannschaft: {', '.join(unknown)}")
    return normalized


def validate_point_values(
    team_ids: Sequence[str],
    point_values: dict[str, Any] | None,
) -> dict[str, Decimal]:
    raw_values = point_values or {}
    if not isinstance(raw_values, dict):
        raise ValueError("Punktwerte müssen je Mannschaft angegeben werden.")
    result: dict[str, Decimal] = {}
    for team_id in team_ids:
        raw_value = raw_values.get(
            team_id,
            TEAM_BY_ID[team_id].default_point_value,
        )
        try:
            value = Decimal(str(raw_value).replace(",", "."))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(
                f"Ungültige Summe pro Punkt für {TEAM_BY_ID[team_id].label}."
            ) from exc
        if not value.is_finite() or value < 0 or value > Decimal("10000"):
            raise ValueError(
                f"Summe pro Punkt für {TEAM_BY_ID[team_id].label} "
                "muss zwischen 0 und 10.000 Euro liegen."
            )
        result[team_id] = value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    return result


def task_configuration(today: date | None = None) -> dict[str, Any]:
    return {
        "seasons": available_seasons(today),
        "teams": [asdict(team) for team in TEAMS],
    }


def run_player_premium_report(
    season: str,
    team_ids: Sequence[str],
    point_values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    start_date, end_date = season_date_range(season)
    selected_ids = validate_team_ids(team_ids)
    selected_point_values = validate_point_values(selected_ids, point_values)
    selected_teams = [TEAM_BY_ID[team_id] for team_id in selected_ids]
    username, password = _load_credentials()

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise PlayerPremiumError(
            "Playwright fehlt. Abhängigkeiten aus requirements.txt installieren."
        ) from exc

    ensure_private_directory(DFBNET_PROFILE_DIR)
    ensure_private_directory(DFBNET_RESULT_DIR)
    logger = logging.getLogger(__name__)
    context = None
    page = None
    try:
        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=str(DFBNET_PROFILE_DIR),
                headless=True,
                accept_downloads=False,
                viewport=None,
            )
            try:
                page = _fresh_page(context)
                page = _login(page, context, username, password)
                del username
                del password
                username = password = ""

                _open_match_report_search(page)
                _apply_match_filters(page, start_date, end_date)
                matches_by_team = _collect_matches(page, selected_teams)
                teams = []
                for team in selected_teams:
                    matches = matches_by_team.get(team.team_id, [])
                    teams.append(
                        _evaluate_team(
                            page,
                            team,
                            matches,
                            selected_point_values[team.team_id],
                        )
                    )

                result = {
                    "season": season,
                    "date_from": start_date.isoformat(),
                    "date_to": end_date.isoformat(),
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "teams": teams,
                    "completeness_warnings": [
                        warning
                        for team_result in teams
                        for warning in team_result.get("completeness", {}).get(
                            "warnings",
                            [],
                        )
                    ],
                }
                _write_result(result)
                return result
            except Exception:
                _save_error_screenshot(page, logger)
                raise
    except PlayerPremiumError:
        raise
    except Exception as exc:
        raise PlayerPremiumError(
            "DFBnet-Auswertung fehlgeschlagen. Die Seite oder ein "
            "Bedienelement konnte nicht eindeutig erkannt werden."
        ) from exc
    finally:
        username = password = ""
        if context is not None:
            try:
                context.close()
            except Exception:
                pass


def build_team_result(
    team: TeamDefinition,
    matches: Sequence[MatchSummary],
    participants_by_match: dict[str, set[str]],
    point_value: Decimal | float | str | None = None,
) -> dict[str, Any]:
    normalized_point_value = validate_point_values(
        (team.team_id,),
        (
            {team.team_id: point_value}
            if point_value is not None
            else None
        ),
    )[team.team_id]
    players = sorted(
        {
            player
            for participants in participants_by_match.values()
            for player in participants
        },
        key=lambda value: value.casefold(),
    )
    rows = []
    team_premium_total = Decimal("0.00")
    for player in players:
        values: dict[str, int | None] = {}
        premium_values: dict[str, float | None] = {}
        total = 0
        premium_total = Decimal("0.00")
        for match in matches:
            if match.outcome == "loss":
                value: int | None = 0
            elif player in participants_by_match.get(match.match_id, set()):
                value = match.points
            else:
                value = None
            values[match.match_id] = value
            if value is not None:
                total += value
                premium = (
                    normalized_point_value * value
                ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                premium_total += premium
                premium_values[match.match_id] = float(premium)
            else:
                premium_values[match.match_id] = None
        team_premium_total += premium_total
        rows.append(
            {
                "name": player,
                "values": values,
                "total": total,
                "premium_values": premium_values,
                "premium_total": float(premium_total),
            }
        )
    return {
        "team_id": team.team_id,
        "label": team.label,
        "dfbnet_name": team.dfbnet_name,
        "point_value": float(normalized_point_value),
        "premium_total": float(team_premium_total),
        "team_points_total": sum(match.points for match in matches),
        "completeness": _match_completeness(team, matches),
        "matches": [
            {
                **{
                    key: value
                    for key, value in asdict(match).items()
                    if key not in {"detail_href", "row_text"}
                },
                "pairing": _match_pairing(team, match),
                "team_points": match.points,
            }
            for match in matches
        ],
        "players": rows,
    }


def parse_match_row(
    cells: Sequence[str],
    team: TeamDefinition,
    *,
    detail_href: str = "",
    row_text: str = "",
    sequence: int = 0,
) -> MatchSummary | None:
    normalized_cells = [_clean_text(value) for value in cells]
    combined = _clean_text(row_text or " | ".join(normalized_cells))
    if not any(
        _cell_matches_team(cell, team.dfbnet_name)
        for cell in normalized_cells
    ):
        return None
    if "freundschaft" in combined.casefold():
        return None

    result_match = re.search(r"(?<!\d)(\d+)\s*:\s*(\d+)(?!\d)", combined)
    if result_match is None:
        return None
    home_score, away_score = (int(value) for value in result_match.groups())
    team_cells = _team_cell_positions(normalized_cells)
    selected_cell = next(
        (
            (index, value)
            for index, value in team_cells
            if _cell_matches_team(value, team.dfbnet_name)
        ),
        None,
    )
    opponent_cell = (
        min(
            (
                item
                for item in team_cells
                if selected_cell is not None and item[0] != selected_cell[0]
            ),
            key=lambda item: abs(item[0] - selected_cell[0]),
            default=None,
        )
        if selected_cell is not None
        else None
    )
    if selected_cell is not None and opponent_cell is not None:
        is_home = selected_cell[0] < opponent_cell[0]
    else:
        team_position = _normalized(combined).find(_normalized(team.dfbnet_name))
        result_position = result_match.start()
        is_home = team_position <= result_position
    own_score, opposing_score = (
        (home_score, away_score) if is_home else (away_score, home_score)
    )
    if own_score > opposing_score:
        outcome, points = "win", 3
    elif own_score == opposing_score:
        outcome, points = "draw", 1
    else:
        outcome, points = "loss", 0

    competition_type = "Pokal" if "pokal" in combined.casefold() else "Meisterschaft"
    round_name = _round_label(combined, competition_type)
    match_date = _extract_date(combined)
    competition = _competition_label(normalized_cells, competition_type)
    selected_team = selected_cell[1] if selected_cell is not None else team.dfbnet_name
    opponent = opponent_cell[1] if opponent_cell is not None else ""
    home_team = selected_team if is_home else opponent
    away_team = opponent if is_home else selected_team
    label = round_name or match_date or f"Spiel {sequence + 1}"
    if competition_type == "Pokal" and round_name:
        label = round_name
    elif round_name:
        label = round_name if round_name.upper().startswith("ST") else f"ST {round_name}"

    identifier_payload = "|".join(
        (team.team_id, match_date, combined, str(sequence))
    )
    match_id = "match_" + _short_hash(identifier_payload)
    return MatchSummary(
        match_id=match_id,
        label=label,
        date=match_date,
        competition=competition,
        competition_type=competition_type,
        round=round_name,
        opponent=opponent,
        result=f"{home_score}:{away_score}",
        outcome=outcome,
        points=points,
        detail_href=detail_href,
        row_text=combined,
        home_team=home_team,
        away_team=away_team,
        is_home=is_home,
    )


def parse_dfbnet_match_row(
    cells: Sequence[str],
    group_text: str,
    team: TeamDefinition,
    *,
    detail_href: str = "",
    sequence: int = 0,
) -> MatchSummary | None:
    normalized_cells = [_clean_text(value) for value in cells]
    group = _clean_text(group_text)
    if len(normalized_cells) < 9:
        return None

    lowered_group = group.casefold()
    if "freundschaft" in lowered_group:
        return None
    if "pokal" in lowered_group:
        competition_type = "Pokal"
    elif "meisterschaft" in lowered_group:
        competition_type = "Meisterschaft"
    else:
        return None

    home_team = normalized_cells[5]
    away_team = normalized_cells[7]
    is_home = _dfbnet_team_matches(home_team, group, team)
    is_away = _dfbnet_team_matches(away_team, group, team)
    if not is_home and not is_away:
        return None

    result_match = re.fullmatch(
        r"(\d+)\s*:\s*(\d+)",
        normalized_cells[8],
    )
    if result_match is None:
        return None
    home_score, away_score = (int(value) for value in result_match.groups())
    own_score, opposing_score = (
        (home_score, away_score) if is_home else (away_score, home_score)
    )
    if own_score > opposing_score:
        outcome, points = "win", 3
    elif own_score == opposing_score:
        outcome, points = "draw", 1
    else:
        outcome, points = "loss", 0

    match_date = _extract_date(normalized_cells[3])
    if competition_type == "Pokal":
        round_name = _round_label(group, competition_type) or "Pokal"
    else:
        matchday = normalized_cells[4]
        round_name = f"ST {matchday}" if matchday else "Meisterschaft"

    opponent = away_team if is_home else home_team
    row_text = _clean_text(" | ".join((group, *normalized_cells)))
    identifier_payload = "|".join(
        (
            team.team_id,
            normalized_cells[2],
            match_date,
            home_team,
            away_team,
            detail_href,
            str(sequence),
        )
    )
    return MatchSummary(
        match_id="match_" + _short_hash(identifier_payload),
        label=round_name,
        date=match_date,
        competition=group or competition_type,
        competition_type=competition_type,
        round=round_name,
        opponent=opponent,
        result=f"{home_score}:{away_score}",
        outcome=outcome,
        points=points,
        detail_href=detail_href,
        row_text=row_text,
        home_team=home_team,
        away_team=away_team,
        is_home=is_home,
    )


def extract_player_names(rows: Iterable[Sequence[str] | str]) -> set[str]:
    names: set[str] = set()
    for row in rows:
        cells = [row] if isinstance(row, str) else list(row)
        for cell in cells:
            candidate = _player_name_candidate(cell)
            if candidate:
                names.add(candidate)
    return names


def _load_credentials() -> tuple[str, str]:
    try:
        from dotenv import dotenv_values
    except ModuleNotFoundError as exc:
        raise PlayerPremiumError(
            "python-dotenv fehlt. Abhängigkeiten aus requirements.txt "
            "installieren."
        ) from exc
    if not SECRETS_PATH.is_file():
        raise PlayerPremiumError(f"Secrets-Datei fehlt: {SECRETS_PATH}")
    values = dotenv_values(
        SECRETS_PATH,
        encoding="utf-8-sig",
        interpolate=False,
    )
    username = values.get("DFBNET_USERNAME")
    password = values.get("DFBNEET_PASSWORD") or values.get("DFBNET_PASSWORD")
    if not isinstance(username, str) or not username:
        raise PlayerPremiumError(
            "Credential-Variable 'DFBNET_USERNAME' fehlt oder ist leer."
        )
    if not isinstance(password, str) or not password:
        raise PlayerPremiumError(
            "Credential-Variable 'DFBNEET_PASSWORD' fehlt oder ist leer."
        )
    return username, password


def _fresh_page(context: Any) -> Any:
    page = context.new_page()
    for existing in list(context.pages):
        if existing is page or existing.is_closed():
            continue
        existing.close()
    return page


def _login(page: Any, context: Any, username: str, password: str) -> Any:
    page.goto(
        DFBNET_LOGIN_URL,
        wait_until="domcontentloaded",
        timeout=60_000,
    )
    page.wait_for_timeout(500)
    _dismiss_cookie_banner(page)
    login_link = page.locator("a[href*='/spielplus/oauth/login']").filter(
        visible=True
    )
    if login_link.count() and login_link.first.is_visible():
        login_link.first.click()
    page.wait_for_timeout(750)
    page = context.pages[-1]
    username_input = _first_visible(
        page,
        ("#username", "input[name='username']", "input[type='text']"),
    )
    password_input = _first_visible(
        page,
        ("#password", "input[name='password']", "input[type='password']"),
    )
    if username_input is not None and password_input is not None:
        username_input.fill(username)
        password_input.fill(password)
        submit = _first_visible(
            page,
            (
                "#kc-login",
                "button[type='submit']",
                "input[type='submit']",
            ),
        )
        if submit is None:
            raise PlayerPremiumError(
                "DFBnet-Anmeldeschaltfläche wurde nicht gefunden."
            )
        submit.click()

    deadline = datetime.now().timestamp() + 180
    while datetime.now().timestamp() < deadline:
        page = context.pages[-1]
        _dismiss_cookie_banner(page)
        if not page.locator("input[type='password']").filter(visible=True).count():
            body = _safe_body_text(page)
            normalized_body = body.casefold()
            if any(
                marker in normalized_body
                for marker in (
                    "spielplus",
                    "spielbericht",
                    "bitte wählen sie die applikation",
                    "session / sitzung",
                    "abmelden",
                )
            ):
                _dismiss_mobile_prompt(page)
                return page
        page.wait_for_timeout(500)
    raise PlayerPremiumError(
        "DFBnet-Login wurde nicht innerhalb von drei Minuten bestätigt."
    )


def _open_match_report_search(page: Any) -> None:
    _dismiss_cookie_banner(page)
    _dismiss_mobile_prompt(page)
    if not _scope_contains(page, re.compile("Wettkampftyp", re.IGNORECASE)):
        reports = page.get_by_text("Spielberichte", exact=True).filter(visible=True)
        if reports.count():
            reports.first.click()
        else:
            toggle = page.locator("#dfb-Menu-toggle").filter(visible=True)
            if toggle.count():
                toggle.first.click()
                page.wait_for_timeout(250)
            menu_link = page.locator(
                "a[href*='mod_sbo/webflow.do?event=START']"
            ).filter(has_text="Spielberichte").filter(visible=True)
            if menu_link.count():
                menu_link.first.click()
            else:
                page.goto(
                    DFBNET_MATCH_REPORT_URL,
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )
        page.wait_for_timeout(1200)
    if not _wait_for_any_text(
        page,
        (re.compile("Wettkampftyp", re.IGNORECASE), re.compile("Mannschaftsart", re.IGNORECASE)),
        30_000,
    ):
        raise PlayerPremiumError(
            "Der Bereich 'Spielberichte' oder seine Filter wurde nicht gefunden."
        )


def _apply_match_filters(page: Any, start_date: date, end_date: date) -> None:
    start = start_date.strftime("%d.%m.%Y")
    end = end_date.strftime("%d.%m.%Y")
    date_inputs = page.locator(
        "input[id^='dfb-Input-datepicker']"
    ).filter(visible=True)
    if date_inputs.count() < 2:
        raise PlayerPremiumError("Datumsfelder der Spielberichtsuche fehlen.")
    for control, value in (
        (date_inputs.nth(0), start),
        (date_inputs.nth(1), end),
    ):
        control.click()
        control.press("Control+A")
        control.type(value)
        control.press("Tab")

    form = page.locator("form[name='actionForm']").filter(visible=True)
    buttons = form.locator("button").filter(visible=True) if form.count() else None
    if buttons is None or not buttons.count():
        raise PlayerPremiumError("Schaltfläche zum Laden der Spielberichte fehlt.")
    buttons.nth(buttons.count() - 1).click()
    page.wait_for_load_state("domcontentloaded", timeout=60_000)
    page.wait_for_timeout(1200)


def _collect_matches(
    page: Any,
    teams: Sequence[TeamDefinition],
) -> dict[str, list[MatchSummary]]:
    collected = {team.team_id: [] for team in teams}
    visited_pages: set[str] = set()
    while True:
        tables = page.locator("table.listtable").filter(visible=True)
        if not tables.count():
            if visited_pages:
                break
            raise PlayerPremiumError("Ergebnistabelle der Spielberichte fehlt.")

        page_signature = _match_table_signature(page, tables)
        if page_signature in visited_pages:
            break
        visited_pages.add(page_signature)

        for table_index in range(tables.count()):
            current_group = ""
            rows = tables.nth(table_index).locator("tr")
            for index in range(rows.count()):
                row = rows.nth(index)
                cells = row.locator("th,td").all_inner_texts()
                if len(cells) == 1:
                    current_group = _clean_text(cells[0])
                    continue
                action = row.locator("a.dfb-link")
                href = ""
                if action.count():
                    raw_href = action.first.get_attribute("href") or ""
                    if raw_href and not raw_href.lower().startswith("javascript:"):
                        href = urljoin(page.url, raw_href)
                for team in teams:
                    parsed = parse_dfbnet_match_row(
                        cells,
                        current_group,
                        team,
                        detail_href=href,
                        sequence=len(collected[team.team_id]),
                    )
                    if parsed is not None:
                        collected[team.team_id].append(parsed)

        if not _go_to_next_page(page):
            break
        page.wait_for_load_state("domcontentloaded", timeout=60_000)
        page.wait_for_timeout(1200)

    for team_id, matches in collected.items():
        unique_matches = _deduplicate_matches(matches)
        unique_matches.sort(key=lambda item: (item.date, item.label, item.match_id))
        collected[team_id] = _deduplicate_labels(unique_matches)
    return collected


def _match_table_signature(page: Any, tables: Any) -> str:
    # The URL may change even when DFBnet returns the same result page again.
    # Only the table contents identify whether pagination actually progressed.
    parts = []
    for index in range(tables.count()):
        try:
            parts.append(_clean_text(tables.nth(index).inner_text(timeout=1_000)))
        except Exception:
            parts.append(f"table-{index}")
    return _short_hash("|".join(parts))


def _deduplicate_matches(matches: Sequence[MatchSummary]) -> list[MatchSummary]:
    result = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for match in matches:
        key = (
            match.date,
            match.home_team,
            match.away_team,
            match.result,
            match.detail_href,
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(match)
    return result


def _evaluate_team(
    page: Any,
    team: TeamDefinition,
    matches: Sequence[MatchSummary],
    point_value: Decimal,
) -> dict[str, Any]:
    participants: dict[str, set[str]] = {}
    list_url = page.url
    for match in matches:
        if match.outcome == "loss":
            participants[match.match_id] = set()
            continue
        try:
            _open_match(page, match, list_url)
            participants[match.match_id] = _match_participants(page, team)
        except Exception:
            participants[match.match_id] = set()
        finally:
            if page.url != list_url:
                page.goto(list_url, wait_until="domcontentloaded", timeout=60_000)
                page.wait_for_timeout(800)
    return build_team_result(team, matches, participants, point_value)


def _open_match(page: Any, match: MatchSummary, list_url: str) -> None:
    if match.detail_href:
        page.goto(match.detail_href, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(2500)
        _dismiss_cookie_banner(page)
        if not _wait_for_selector(page, "#navTab0", 30_000):
            raise PlayerPremiumError("Spielbericht wurde nicht vollständig geladen.")
        return
    page.goto(list_url, wait_until="domcontentloaded", timeout=60_000)
    for row in _all_table_rows(page):
        if _normalized(match.row_text) not in _normalized(row.inner_text()):
            continue
        action = _row_action(row)
        if action is not None:
            action.click()
            page.wait_for_timeout(900)
            return
    raise PlayerPremiumError("Spielbericht konnte nicht geöffnet werden.")


def _match_participants(page: Any, team: TeamDefinition) -> set[str]:
    teams_url = _report_detail_url(page.url, "teams")
    if not teams_url:
        raise PlayerPremiumError("Mannschaftsroute des Spielberichts fehlt.")
    page.goto(teams_url, wait_until="domcontentloaded", timeout=60_000)
    if not _wait_for_selector(page, ".panel.team", 30_000):
        raise PlayerPremiumError("Mannschaften des Spielberichts fehlen.")

    panel = _team_panel(page, team)
    if panel is None:
        return set()
    lineup = panel.locator(".team-lineup")
    if not lineup.count() or "collapse-in" not in (lineup.first.get_attribute("class") or ""):
        panel.locator(".panel-heading").first.click()
        page.wait_for_timeout(500)

    player_lists = panel.locator(".team-player-list .player-list")
    if not player_lists.count():
        return set()
    starter_names = player_lists.first.locator(
        ".player-name"
    ).all_inner_texts()
    starters = {
        _clean_text(name)
        for name in starter_names
        if _clean_text(name)
    }

    flow_tab = page.locator("#navTab2").filter(visible=True)
    if not flow_tab.count():
        return starters
    try:
        flow_tab.first.click(timeout=5_000)
    except Exception:
        return starters
    if not _wait_for_selector(page, ".panel.substitution", 30_000):
        return starters
    return starters | _substitution_names(page, team)


def _names_from_section(page: Any, heading_pattern: re.Pattern[str]) -> set[str]:
    for scope in _scopes(page):
        headings = scope.get_by_text(heading_pattern).filter(visible=True)
        for index in range(headings.count()):
            heading = headings.nth(index)
            table = heading.locator("xpath=following::table[1]")
            if table.count():
                return extract_player_names(_table_cell_rows(table.first))
            container = heading.locator(
                "xpath=ancestor::*[self::section or self::fieldset or "
                "contains(@class,'panel') or contains(@class,'card')][1]"
            )
            if container.count():
                rows = container.first.locator("tr,li")
                return extract_player_names(
                    [_clean_text(rows.nth(i).inner_text()) for i in range(rows.count())]
                )
    return set()


def _substitution_names(page: Any, team: TeamDefinition) -> set[str]:
    team_names = page.locator(
        ".panel-heading-match .team-info--name"
    ).all_inner_texts()
    selected_index = next(
        (
            index
            for index, name in enumerate(team_names)
            if _dfbnet_team_matches(
                name,
                _safe_body_text(page),
                team,
            )
        ),
        None,
    )
    if selected_index is None:
        return set()
    selected_is_away = selected_index == 1

    result = set()
    events = page.locator(".panel.substitution .event-header")
    for index in range(events.count()):
        event = events.nth(index)
        classes = (event.get_attribute("class") or "").split()
        if ("away" in classes) != selected_is_away:
            continue
        names = event.locator(".person-name").all_inner_texts()
        if names:
            incoming = _clean_text(names[0])
            if incoming:
                result.add(incoming)
    return result


def _team_panel(page: Any, team: TeamDefinition) -> Any | None:
    panels = page.locator(".panel.team")
    for index in range(panels.count()):
        panel = panels.nth(index)
        heading = panel.locator("h4.media-heading")
        if heading.count() and _dfbnet_team_matches(
            heading.first.inner_text(),
            panel.inner_text(),
            team,
        ):
            return panel
    return None


def _report_detail_url(current_url: str, suffix: str) -> str:
    match = re.search(
        r"(.+?#/match-report/report-details/[^/]+)(?:/.*)?$",
        current_url,
    )
    return f"{match.group(1)}/{suffix}" if match else ""


def _all_table_rows(page: Any) -> list[Any]:
    result = []
    for scope in _scopes(page):
        rows = scope.locator("table tbody tr").filter(visible=True)
        result.extend(rows.nth(index) for index in range(rows.count()))
    return result


def _table_cell_rows(table: Any) -> list[list[str]]:
    rows = table.locator("tbody tr")
    return [
        [_clean_text(value) for value in rows.nth(index).locator("th,td").all_inner_texts()]
        for index in range(rows.count())
    ]


def _row_detail_href(row: Any, base_url: str) -> str:
    action = _row_action(row)
    if action is None:
        return ""
    href = action.get_attribute("href") or ""
    return "" if not href or href.lower().startswith("javascript:") else urljoin(base_url, href)


def _row_action(row: Any) -> Any | None:
    candidates = row.locator("a,button,input[type='button'],input[type='image']")
    scored = []
    for index in range(candidates.count()):
        candidate = candidates.nth(index)
        if not candidate.is_visible():
            continue
        description = " ".join(
            filter(
                None,
                (
                    candidate.get_attribute("title"),
                    candidate.get_attribute("aria-label"),
                    candidate.get_attribute("alt"),
                    candidate.inner_text(),
                ),
            )
        ).casefold()
        score = sum(
            token in description
            for token in ("spielbericht", "bearbeiten", "öffnen", "oeffnen", "stift")
        )
        if score:
            scored.append((score, candidate))
    return max(scored, key=lambda item: item[0])[1] if scored else None


def _go_to_next_page(page: Any) -> bool:
    for scope in _scopes(page):
        explicit = _next_page_control(scope)
        if explicit is not None:
            explicit.click()
            return True
        numbered = _next_numbered_page_control(scope, page)
        if numbered is not None:
            numbered.click()
            return True
        candidates = scope.get_by_role(
            "link",
            name=re.compile(r"^(Weiter|Nächste|Naechste|>)$", re.IGNORECASE),
        ).filter(visible=True)
        if not candidates.count():
            candidates = scope.locator(
                "a[rel='next'],button[aria-label*='ächste'],"
                "button[title*='ächste']"
            ).filter(visible=True)
        if candidates.count():
            candidate = candidates.first
            if candidate.get_attribute("aria-disabled") == "true":
                return False
            classes = candidate.get_attribute("class") or ""
            if "disabled" in classes.casefold():
                return False
            candidate.click()
            return True
    return False


def _next_page_control(scope: Any) -> Any | None:
    controls = scope.locator("a,button,input[type='button'],input[type='submit']").filter(
        visible=True
    )
    for index in range(controls.count()):
        control = controls.nth(index)
        if _is_disabled_control(control):
            continue
        description = _control_description(control)
        if re.search(
            r"\b(weiter|naechste|n(?:ae|\u00e4)chste|next)\b|^[>\u203a\u00bb]+$",
            description,
            re.IGNORECASE,
        ):
            return control
        rel = str(control.get_attribute("rel") or "").casefold()
        if rel == "next":
            return control
    return None


def _next_numbered_page_control(scope: Any, page: Any) -> Any | None:
    current = _current_result_page_number(scope, page)
    controls = scope.locator("a,button").filter(visible=True)
    numeric_controls: list[tuple[int, Any]] = []
    for index in range(controls.count()):
        control = controls.nth(index)
        if _is_disabled_control(control):
            continue
        text = _clean_text(control.inner_text())
        if re.fullmatch(r"\d{1,3}", text):
            numeric_controls.append((int(text), control))
    if not numeric_controls:
        return None
    if current is not None:
        for number, control in sorted(numeric_controls, key=lambda item: item[0]):
            if number == current + 1:
                return control
        return None
    greater_than_one = [item for item in numeric_controls if item[0] > 1]
    return min(greater_than_one, key=lambda item: item[0])[1] if greater_than_one else None


def _current_result_page_number(scope: Any, page: Any) -> int | None:
    body_match = re.search(
        r"\bSeite\s+(\d{1,3})\s+(?:von|/)\s+\d{1,3}\b",
        _safe_body_text(page),
        re.IGNORECASE,
    )
    if body_match:
        return int(body_match.group(1))
    active = scope.locator(
        "[aria-current='page'],.active,.current,.selected,.ui-state-active"
    ).filter(visible=True)
    for index in range(active.count()):
        text = _clean_text(active.nth(index).inner_text())
        if re.fullmatch(r"\d{1,3}", text):
            return int(text)
    return None


def _is_disabled_control(control: Any) -> bool:
    if control.get_attribute("aria-disabled") == "true":
        return True
    if control.get_attribute("disabled") is not None:
        return True
    classes = str(control.get_attribute("class") or "").casefold()
    return any(token in classes for token in ("disabled", "inactive"))


def _control_description(control: Any) -> str:
    values = []
    for attribute in ("title", "aria-label", "alt", "value"):
        value = control.get_attribute(attribute)
        if value:
            values.append(str(value))
    try:
        values.append(control.inner_text())
    except Exception:
        pass
    return _clean_text(" ".join(values)).casefold()


def _fill_labeled(page: Any, label: re.Pattern[str], value: str) -> bool:
    for scope in _scopes(page):
        controls = scope.get_by_label(label).filter(visible=True)
        if controls.count():
            controls.first.fill(value)
            return True
    return False


def _fill_date_input(page: Any, index: int, value: str) -> bool:
    for scope in _scopes(page):
        controls = scope.locator(
            "input[type='date'],input[type='text'][name*='datum' i],"
            "input[type='text'][name*='date' i]"
        ).filter(visible=True)
        if controls.count() > index:
            controls.nth(index).fill(value)
            return True
    return False


def _select_first_option(
    page: Any,
    label: re.Pattern[str],
    *,
    empty: bool,
) -> bool:
    for scope in _scopes(page):
        controls = scope.get_by_label(label).filter(visible=True)
        if not controls.count():
            continue
        control = controls.first
        if control.evaluate("element => element.tagName") != "SELECT":
            continue
        options = control.locator("option")
        values = [
            (options.nth(index).get_attribute("value") or "", options.nth(index).inner_text())
            for index in range(options.count())
        ]
        if empty:
            target = next(
                (value for value, text in values if not value or "keine" in text.casefold()),
                values[0][0] if values else "",
            )
        else:
            target = next(
                (
                    value
                    for value, text in values
                    if value and "keine" not in text.casefold()
                ),
                "",
            )
        control.select_option(value=target)
        return True
    return False


def _click_text(
    page: Any,
    pattern: re.Pattern[str],
    *,
    roles: Sequence[str] = ("link", "button"),
) -> bool:
    for scope in _scopes(page):
        for role in roles:
            try:
                candidates = scope.get_by_role(role, name=pattern).filter(visible=True)
            except Exception:
                continue
            if candidates.count():
                candidates.first.click()
                return True
        candidates = scope.get_by_text(pattern, exact=True).filter(visible=True)
        if candidates.count():
            candidates.first.click()
            return True
    return False


def _wait_for_any_text(
    page: Any,
    patterns: Sequence[re.Pattern[str]],
    timeout_ms: int,
) -> bool:
    deadline = datetime.now().timestamp() + timeout_ms / 1000
    while datetime.now().timestamp() < deadline:
        body = _safe_body_text(page)
        if any(pattern.search(body) for pattern in patterns):
            return True
        page.wait_for_timeout(250)
    return False


def _wait_for_selector(page: Any, selector: str, timeout_ms: int) -> bool:
    deadline = datetime.now().timestamp() + timeout_ms / 1000
    while datetime.now().timestamp() < deadline:
        locator = page.locator(selector)
        if locator.count() and locator.first.is_visible():
            return True
        page.wait_for_timeout(250)
    return False


def _dismiss_cookie_banner(page: Any) -> None:
    try:
        buttons = page.get_by_text("Alle Ablehnen", exact=True).filter(
            visible=True
        )
        if buttons.count():
            buttons.first.click(force=True, timeout=2_000)
            page.wait_for_timeout(250)
    except Exception:
        pass


def _dismiss_mobile_prompt(page: Any) -> None:
    try:
        buttons = page.get_by_text("Nein", exact=True).filter(visible=True)
        if buttons.count():
            buttons.first.click(timeout=2_000)
            page.wait_for_timeout(250)
    except Exception:
        pass


def _scope_contains(page: Any, pattern: re.Pattern[str]) -> bool:
    return bool(pattern.search(_safe_body_text(page)))


def _safe_body_text(page: Any) -> str:
    texts = []
    for scope in _scopes(page):
        try:
            texts.append(scope.locator("body").inner_text(timeout=500))
        except Exception:
            pass
    return "\n".join(texts)


def _scopes(page: Any) -> list[Any]:
    return [page, *[frame for frame in page.frames if frame != page.main_frame]]


def _first_visible(page: Any, selectors: Sequence[str]) -> Any | None:
    for selector in selectors:
        locator = page.locator(selector).filter(visible=True)
        if locator.count():
            return locator.first
    return None


def _deduplicate_labels(matches: Sequence[MatchSummary]) -> list[MatchSummary]:
    counts: dict[str, int] = {}
    result = []
    for match in matches:
        count = counts.get(match.label, 0) + 1
        counts[match.label] = count
        if count == 1:
            result.append(match)
            continue
        result.append(
            MatchSummary(
                **{
                    **asdict(match),
                    "label": f"{match.label} ({count})",
                }
            )
        )
    return result


def _match_pairing(team: TeamDefinition, match: MatchSummary) -> str:
    home = _clean_text(match.home_team)
    away = _clean_text(match.away_team)
    if home and away:
        return f"{home} - {away}"
    opponent = _clean_text(match.opponent)
    if opponent:
        return f"{team.label} - {opponent}"
    return team.label


def _match_completeness(
    team: TeamDefinition,
    matches: Sequence[MatchSummary],
) -> dict[str, Any]:
    matchdays = sorted(
        {
            number
            for number in (_matchday_number(match) for match in matches)
            if number is not None
        }
    )
    warnings = []
    missing: list[int] = []
    if len(matchdays) >= 2:
        expected = set(range(matchdays[0], matchdays[-1] + 1))
        missing = sorted(expected - set(matchdays))
    if missing:
        warnings.append(
            f"{team.label}: fehlende Spieltage "
            + ", ".join(str(value) for value in missing)
            + ". Bitte DFBnet-Ergebnisliste/Pagination pruefen."
        )
    return {
        "status": "warning" if warnings else "complete",
        "matchdays": matchdays,
        "missing_matchdays": missing,
        "warnings": warnings,
    }


def _matchday_number(match: MatchSummary) -> int | None:
    if match.competition_type != "Meisterschaft":
        return None
    for value in (match.round, match.label):
        parsed = _matchday_number_from_text(value)
        if parsed is not None:
            return parsed
    return None


def _matchday_number_from_text(value: str) -> int | None:
    match = re.search(r"(?:(\d+)\.?\s*ST\b|\bST\s*(\d+))", value, re.IGNORECASE)
    if not match:
        return None
    return int(next(item for item in match.groups() if item))


def _round_label(text: str, competition_type: str) -> str:
    if competition_type == "Meisterschaft":
        match = re.search(
            r"(?:(\d+)\.?\s*ST\b|\bST\s*(\d+))",
            text,
            re.IGNORECASE,
        )
        if match:
            return f"ST {next(value for value in match.groups() if value)}"
        return ""
    match = re.search(
        r"\b(Finale|Halbfinale|Viertelfinale|Achtelfinale|"
        r"Zwischenrunde|Qualifikation|(?:\d+)\.\s*Runde|"
        r"Runde\s+\d+)\b",
        text,
        re.IGNORECASE,
    )
    return _clean_text(match.group(1)) if match else ""


def _extract_date(text: str) -> str:
    match = re.search(r"\b(\d{2})\.(\d{2})\.(\d{4})\b", text)
    if not match:
        return ""
    day, month, year = match.groups()
    return f"{year}-{month}-{day}"


def _competition_label(cells: Sequence[str], fallback: str) -> str:
    for cell in cells:
        lowered = cell.casefold()
        if "meisterschaft" in lowered or "pokal" in lowered:
            return cell
    return fallback


def _team_cell_positions(cells: Sequence[str]) -> list[tuple[int, str]]:
    result = []
    for index, cell in enumerate(cells):
        cleaned = _clean_text(cell)
        if not cleaned:
            continue
        lowered = cleaned.casefold()
        if any(
            token in lowered
            for token in (
                "meisterschaft",
                "pokal",
                "freundschaft",
                "spieltag",
                "beendet",
                "abgesetzt",
            )
        ):
            continue
        if re.search(r"(?:(\d+)\.?\s*ST\b|\bST\s*(\d+))", cleaned, re.IGNORECASE):
            continue
        if re.fullmatch(r"\d+\s*:\s*\d+", cleaned):
            continue
        if re.fullmatch(r"\d{2}\.\d{2}\.\d{4}.*", cleaned):
            continue
        words = re.findall(r"[A-Za-zÄÖÜäöüßÀ-ÿ][\wÄÖÜäöüßÀ-ÿ.'’-]*", cleaned)
        if len(words) >= 2 and len(cleaned) >= 4:
            result.append((index, cleaned))
    return result


def _player_name_candidate(value: str) -> str:
    text = _clean_text(value)
    if not text:
        return ""
    text = re.sub(r"^\s*\d{1,3}[.)]?\s+", "", text)
    text = re.sub(
        r"\s*\((?:C|K|TW|ETW|Spielführer|Kapitän)\)\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = _clean_text(text)
    lowered = text.casefold()
    excluded = (
        "startaufstellung",
        "ersatzbank",
        "spieler",
        "mannschaft",
        "einwechslung",
        "auswechslung",
        "spielminute",
        "minute",
        "position",
        "trikot",
        "nummer",
        "bsv viktoria bielstein",
    )
    if any(token in lowered for token in excluded):
        return ""
    if re.search(r"\d{2}\.\d{2}\.\d{4}", text):
        return ""
    words = re.findall(r"[A-Za-zÄÖÜäöüßÀ-ÿ][A-Za-zÄÖÜäöüßÀ-ÿ'’.-]+", text)
    if len(words) < 2 or len(words) > 6:
        return ""
    candidate = " ".join(words)
    if len(candidate) < 5 or len(candidate) > 100:
        return ""
    return candidate


def _contains_team(text: str, team_name: str) -> bool:
    segments = re.split(r"[|\n\r]+", str(text or ""))
    return any(_cell_matches_team(segment, team_name) for segment in segments)


def _dfbnet_team_matches(
    value: str,
    competition_context: str,
    team: TeamDefinition,
) -> bool:
    category = _competition_category(competition_context)
    suffix = _dfbnet_club_suffix(value)
    if suffix is None:
        return False
    if category == "frauen":
        return team.team_id == "damen" and suffix in {"", "frauen"}
    if category == "herren":
        if team.team_id == "herren_1":
            return suffix in {"", "i"}
        if team.team_id == "herren_2":
            return suffix == "ii"
    return False


def _competition_category(value: str) -> str:
    normalized = _normalized(value)
    has_frauen = bool(re.search(r"\b(frauen|damen)\b", normalized))
    has_herren = bool(re.search(r"\bherren\b", normalized))
    if has_frauen and not has_herren:
        return "frauen"
    if has_herren and not has_frauen:
        return "herren"
    first_segment = re.split(r"[,|\n\r]+", normalized, maxsplit=1)[0]
    if re.search(r"\b(frauen|damen)\b", first_segment):
        return "frauen"
    if re.search(r"\bherren\b", first_segment):
        return "herren"
    return ""


def _dfbnet_club_suffix(value: str) -> str | None:
    normalized_value = _normalized(value)
    normalized_club = _normalized(DFBNET_CLUB_NAME)
    if normalized_value == normalized_club:
        return ""
    if not normalized_value.startswith(normalized_club):
        return None
    suffix = normalized_value[len(normalized_club) :].strip(" -–—,;:()")
    suffix = re.sub(r"\s+(heim|gast)$", "", suffix).strip()
    return suffix


def _cell_matches_team(value: str, team_name: str) -> bool:
    normalized_value = _normalized(value)
    normalized_team = _normalized(team_name)
    if normalized_value == normalized_team:
        return True
    if not normalized_value.startswith(normalized_team):
        return False
    suffix = normalized_value[len(normalized_team) :].strip(" -–—,;:()")
    return not suffix or suffix.startswith(("heim", "gast"))


def _normalized(value: str) -> str:
    cleaned = re.sub(r"[\u00ad\u200b-\u200d\ufeff]", "", str(value or ""))
    return re.sub(r"\s+", " ", cleaned).strip().casefold()


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _short_hash(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _write_result(result: dict[str, Any]) -> None:
    season_name = result["season"].replace("/", "_")
    paths = (
        DFBNET_RESULT_DIR / f"spieler_praemien_{season_name}.json",
        DFBNET_RESULT_DIR / "spieler_praemien_zuletzt.json",
    )
    content = json.dumps(result, ensure_ascii=False, indent=2)
    for path in paths:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
        protect_file(path)


def _save_error_screenshot(page: Any | None, logger: logging.Logger) -> None:
    if page is None or page.is_closed():
        return
    try:
        screenshot_dir = ensure_private_directory(
            PROJECT_ROOT / ".runtime" / "screenshots"
        )
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        path = screenshot_dir / f"dfbnet_player_premiums_{timestamp}.png"
        page.screenshot(
            path=str(path),
            full_page=False,
            mask=[
                page.locator("#username,input[name='username']"),
                page.locator("input[type='password']"),
            ],
            mask_color="#000000",
        )
        protect_file(path)
    except Exception as exc:
        logger.warning("DFBnet-Fehler-Screenshot fehlgeschlagen: %s", exc)
