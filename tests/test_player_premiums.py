import unittest
from datetime import date
from decimal import Decimal

from banking_dashboard.player_premiums import (
    TEAM_BY_ID,
    MatchSummary,
    available_seasons,
    build_team_result,
    extract_player_names,
    parse_dfbnet_match_row,
    parse_match_row,
    season_date_range,
    task_configuration,
    validate_point_values,
    validate_team_ids,
)


class PlayerPremiumConfigurationTests(unittest.TestCase):
    def test_available_seasons_start_in_july_and_end_at_2022(self):
        self.assertEqual(
            available_seasons(date(2026, 6, 12)),
            ["2025/2026", "2024/2025", "2023/2024", "2022/2023"],
        )
        self.assertEqual(available_seasons(date(2026, 7, 1))[0], "2026/2027")

    def test_season_range_runs_from_july_to_june(self):
        self.assertEqual(
            season_date_range("2025/2026"),
            (date(2025, 7, 1), date(2026, 6, 30)),
        )
        for invalid in ("2025", "2025/2027", "2021/2022"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    season_date_range(invalid)

    def test_only_known_teams_are_accepted(self):
        self.assertEqual(
            validate_team_ids(["herren_1", "damen", "herren_1"]),
            ("herren_1", "damen"),
        )
        with self.assertRaises(ValueError):
            validate_team_ids(["andere_mannschaft"])

    def test_default_point_values_are_exposed_and_validated(self):
        teams = {
            team["team_id"]: team
            for team in task_configuration(date(2026, 6, 12))["teams"]
        }
        self.assertEqual(teams["herren_1"]["default_point_value"], 5.0)
        self.assertEqual(teams["herren_2"]["default_point_value"], 2.5)
        self.assertEqual(teams["damen"]["default_point_value"], 2.5)
        self.assertEqual(
            validate_point_values(
                ("herren_1", "herren_2"),
                {"herren_1": "6,25", "herren_2": "2.50"},
            ),
            {
                "herren_1": Decimal("6.25"),
                "herren_2": Decimal("2.50"),
            },
        )


class PlayerPremiumEvaluationTests(unittest.TestCase):
    def test_match_rows_determine_home_and_away_points(self):
        team = TEAM_BY_ID["herren_1"]
        home_win = parse_match_row(
            [
                "Meisterschaft",
                "1. ST",
                "10.08.2025",
                team.dfbnet_name,
                "SV Testdorf 1910 e.V.",
                "2:1",
            ],
            team,
        )
        away_loss = parse_match_row(
            [
                "Pokal",
                "Achtelfinale",
                "17.08.2025",
                "SV Testdorf 1910 e.V.",
                team.dfbnet_name,
                "3:1",
            ],
            team,
        )

        self.assertEqual(home_win.outcome, "win")
        self.assertEqual(home_win.points, 3)
        self.assertEqual(home_win.label, "ST 1")
        self.assertEqual(home_win.opponent, "SV Testdorf 1910 e.V.")
        self.assertEqual(home_win.home_team, team.dfbnet_name)
        self.assertEqual(home_win.away_team, "SV Testdorf 1910 e.V.")
        self.assertEqual(away_loss.outcome, "loss")
        self.assertEqual(away_loss.points, 0)
        self.assertEqual(away_loss.label, "Achtelfinale")
        self.assertEqual(away_loss.home_team, "SV Testdorf 1910 e.V.")
        self.assertEqual(away_loss.away_team, team.dfbnet_name)

    def test_friendlies_and_rows_without_result_are_ignored(self):
        team = TEAM_BY_ID["damen"]
        self.assertIsNone(
            parse_match_row(
                [
                    "Freundschaftsspiel",
                    "01.07.2025",
                    team.dfbnet_name,
                    "Testgegner Frauen",
                    "1:1",
                ],
                team,
            )
        )
        self.assertIsNone(
            parse_match_row(
                ["Meisterschaft", team.dfbnet_name, "Testgegner Frauen"],
                team,
            )
        )

    def test_dfbnet_result_rows_use_group_and_fixed_columns(self):
        team = TEAM_BY_ID["herren_2"]
        match = parse_dfbnet_match_row(
            [
                "",
                "",
                "009",
                "So.\n31.08.2025\n15:15",
                "1",
                "TuS Reichshof 1883 / 1929 e.V.",
                "-",
                team.dfbnet_name,
                "1 : 1",
                "",
            ],
            (
                "Herren, Kreisliga C, Kreis Berg\n"
                "230566 - Meisterschaft, Kreisliga C 6"
            ),
            team,
            detail_href="/match-report/009",
        )

        self.assertIsNotNone(match)
        self.assertEqual(match.label, "ST 1")
        self.assertEqual(match.date, "2025-08-31")
        self.assertEqual(match.opponent, "TuS Reichshof 1883 / 1929 e.V.")
        self.assertEqual(match.home_team, "TuS Reichshof 1883 / 1929 e.V.")
        self.assertEqual(match.away_team, team.dfbnet_name)
        self.assertEqual(match.outcome, "draw")
        self.assertEqual(match.points, 1)

    def test_dfbnet_pokal_round_comes_from_group_header(self):
        team = TEAM_BY_ID["damen"]
        match = parse_dfbnet_match_row(
            [
                "",
                "",
                "003",
                "Mi.\n10.09.2025\n19:30",
                "1",
                team.dfbnet_name,
                "-",
                "SV Testdorf Frauen",
                "2 : 0",
                "",
            ],
            (
                "Frauen, Kreispokal, Kreis Berg\n"
                "280006 - Kreispokal der Frauen 2025 / 26, Runde 1"
            ),
            team,
        )

        self.assertIsNotNone(match)
        self.assertEqual(match.label, "Runde 1")
        self.assertEqual(match.competition_type, "Pokal")
        self.assertEqual(match.outcome, "win")

    def test_dfbnet_friendship_group_is_ignored(self):
        team = TEAM_BY_ID["damen"]
        self.assertIsNone(
            parse_dfbnet_match_row(
                [
                    "",
                    "",
                    "001",
                    "01.07.2025",
                    "1",
                    team.dfbnet_name,
                    "-",
                    "SV Testdorf Frauen",
                    "3 : 1",
                    "",
                ],
                "Frauen, Kreisfreundschaftsspiele - Freundschaftsspiel",
                team,
            )
        )

    def test_historical_bare_name_is_assigned_by_competition_category(self):
        bare_name = "BSV Viktoria Bielstein 1920 e.V."
        cells = [
            "",
            "",
            "003",
            "10.09.2022",
            "2",
            bare_name,
            "-",
            "SV Testdorf",
            "2 : 0",
            "",
        ]

        women_match = parse_dfbnet_match_row(
            cells,
            "Frauen, Bezirksliga - Meisterschaft",
            TEAM_BY_ID["damen"],
        )
        women_as_men = parse_dfbnet_match_row(
            cells,
            "Frauen, Bezirksliga - Meisterschaft",
            TEAM_BY_ID["herren_1"],
        )
        men_match = parse_dfbnet_match_row(
            cells,
            "Herren, Kreisliga B - Meisterschaft",
            TEAM_BY_ID["herren_1"],
        )
        men_as_women = parse_dfbnet_match_row(
            cells,
            "Herren, Kreisliga B - Meisterschaft",
            TEAM_BY_ID["damen"],
        )

        self.assertIsNotNone(women_match)
        self.assertIsNone(women_as_men)
        self.assertIsNotNone(men_match)
        self.assertIsNone(men_as_women)

    def test_herren_roman_suffix_selects_first_or_second_team(self):
        base_cells = [
            "",
            "",
            "004",
            "17.09.2022",
            "3",
            "",
            "-",
            "SV Testdorf",
            "1 : 1",
            "",
        ]
        group = "Herren, Kreisliga - Meisterschaft"

        first_with_i = list(base_cells)
        first_with_i[5] = "BSV Viktoria Bielstein 1920 e.V. I"
        second_with_ii = list(base_cells)
        second_with_ii[5] = "BSV Viktoria Bielstein 1920 e.V. II"
        ignored_third = list(base_cells)
        ignored_third[5] = "BSV Viktoria Bielstein 1920 e.V. III"

        self.assertIsNotNone(
            parse_dfbnet_match_row(
                first_with_i,
                group,
                TEAM_BY_ID["herren_1"],
            )
        )
        self.assertIsNone(
            parse_dfbnet_match_row(
                first_with_i,
                group,
                TEAM_BY_ID["herren_2"],
            )
        )
        self.assertIsNotNone(
            parse_dfbnet_match_row(
                second_with_ii,
                group,
                TEAM_BY_ID["herren_2"],
            )
        )
        for team_id in ("herren_1", "herren_2", "damen"):
            self.assertIsNone(
                parse_dfbnet_match_row(
                    ignored_third,
                    group,
                    TEAM_BY_ID[team_id],
                )
            )

    def test_first_team_does_not_match_second_team_name(self):
        first_team = TEAM_BY_ID["herren_1"]
        second_team = TEAM_BY_ID["herren_2"]

        self.assertIsNone(
            parse_match_row(
                [
                    "Meisterschaft",
                    "1. ST",
                    second_team.dfbnet_name,
                    "SV Testdorf 1910 e.V.",
                    "2:1",
                ],
                first_team,
            )
        )

    def test_matrix_uses_blank_for_non_participation_and_zero_for_losses(self):
        team = TEAM_BY_ID["herren_2"]
        matches = (
            MatchSummary(
                "match_win",
                "ST 1",
                "2025-08-10",
                "Meisterschaft",
                "Meisterschaft",
                "ST 1",
                "Gegner A",
                "2:0",
                "win",
                3,
                "",
                "",
            ),
            MatchSummary(
                "match_loss",
                "ST 2",
                "2025-08-17",
                "Meisterschaft",
                "Meisterschaft",
                "ST 2",
                "Gegner B",
                "0:1",
                "loss",
                0,
                "",
                "",
            ),
        )

        result = build_team_result(
            team,
            matches,
            {
                "match_win": {"Max Mustermann"},
                "match_loss": {"Erika Beispiel"},
            },
            "2.50",
        )
        rows = {row["name"]: row for row in result["players"]}

        self.assertEqual(rows["Max Mustermann"]["values"]["match_win"], 3)
        self.assertEqual(rows["Max Mustermann"]["values"]["match_loss"], 0)
        self.assertIsNone(rows["Erika Beispiel"]["values"]["match_win"])
        self.assertEqual(rows["Erika Beispiel"]["values"]["match_loss"], 0)
        self.assertEqual(rows["Max Mustermann"]["total"], 3)
        self.assertEqual(
            rows["Max Mustermann"]["premium_values"]["match_win"],
            7.5,
        )
        self.assertEqual(rows["Max Mustermann"]["premium_total"], 7.5)
        self.assertEqual(result["point_value"], 2.5)
        self.assertEqual(result["team_points_total"], 3)
        self.assertEqual(result["matches"][0]["pairing"], "BSV - Herren 2 - Gegner A")
        self.assertEqual(result["matches"][0]["team_points"], 3)

    def test_completeness_warns_about_missing_matchdays(self):
        team = TEAM_BY_ID["herren_1"]
        matches = (
            MatchSummary(
                "match_10",
                "ST 10",
                "2025-10-10",
                "Meisterschaft",
                "Meisterschaft",
                "ST 10",
                "Gegner A",
                "1:0",
                "win",
                3,
                "",
                "",
            ),
            MatchSummary(
                "match_13",
                "ST 13",
                "2025-10-31",
                "Meisterschaft",
                "Meisterschaft",
                "ST 13",
                "Gegner B",
                "2:0",
                "win",
                3,
                "",
                "",
            ),
        )

        result = build_team_result(
            team,
            matches,
            {"match_10": {"Max Mustermann"}, "match_13": {"Max Mustermann"}},
            "5.00",
        )

        self.assertEqual(
            result["completeness"]["missing_matchdays"],
            [11, 12],
        )
        self.assertEqual(result["completeness"]["status"], "warning")

    def test_player_names_exclude_headers_and_numbers(self):
        self.assertEqual(
            extract_player_names(
                [
                    ["9 Max Mustermann"],
                    ["Ersatzbank"],
                    ["17 Erika Beispiel (C)"],
                    ["45. Minute"],
                ]
            ),
            {"Max Mustermann", "Erika Beispiel"},
        )


if __name__ == "__main__":
    unittest.main()
