import json
import unittest

from banking_dashboard.player_payments import (
    MemberCandidate,
    _set_current_private_result,
    _public_review,
    apply_player_payment_offsets,
    clear_player_payment_session,
    eligible_premium_players,
    export_player_payment_files,
    load_current_player_payment_review,
    mask_iban,
    match_member_name,
    save_manual_player_payment,
    validate_bic,
    validate_iban,
    validate_payment_data,
)


class PlayerPaymentMatchingTests(unittest.TestCase):
    def test_source_name_order_is_an_exact_match(self):
        candidate = MemberCandidate(
            "1",
            "Mustermann",
            "Max",
            "https://verein.dfbnet.org/member/1",
        )

        result = match_member_name("Mustermann Max", [candidate])

        self.assertEqual(result["quality"], "exakt")
        self.assertEqual(result["status"], "eindeutig_gefunden")
        self.assertEqual(result["member_name"], "Max Mustermann")

    def test_umlauts_accents_hyphens_and_order_are_normalized(self):
        candidate = MemberCandidate(
            "1",
            "Núñez-Müller",
            "José Luis",
            "https://verein.dfbnet.org/member/1",
        )

        result = match_member_name("Jose Luis Nunez Mueller", [candidate])

        self.assertEqual(result["quality"], "normalisiert")
        self.assertEqual(result["status"], "eindeutig_gefunden")

    def test_duplicate_normalized_names_require_manual_review(self):
        candidates = [
            MemberCandidate(
                str(index),
                "Müller",
                "Anna",
                f"https://verein.dfbnet.org/member/{index}",
            )
            for index in (1, 2)
        ]

        result = match_member_name("Anna Mueller", candidates)

        self.assertEqual(result["quality"], "mehrdeutig")
        self.assertEqual(result["status"], "manuell_pruefen")
        self.assertIsNone(result["candidate"])
        self.assertEqual(result["candidate_count"], 2)

    def test_similar_name_is_not_automatically_selected(self):
        candidate = MemberCandidate(
            "1",
            "Musterman",
            "Max",
            "https://verein.dfbnet.org/member/1",
        )

        result = match_member_name("Max Mustermann", [candidate])

        self.assertEqual(result["quality"], "ähnlich")
        self.assertEqual(result["status"], "manuell_pruefen")


class PlayerPaymentValidationTests(unittest.TestCase):
    def test_valid_iban_is_normalized_and_checked_with_mod97(self):
        result = validate_iban("de89 3704 0044 0532 0130 00")

        self.assertEqual(result["normalized"], "DE89370400440532013000")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country"], "DE")

    def test_invalid_iban_length_checksum_and_characters_are_rejected(self):
        result = validate_iban("DE89-3704-0044-0532-0130-01!")

        self.assertFalse(result["valid"])
        self.assertIn("unzulässige_zeichen", result["errors"])

    def test_bic_format_and_country_consistency_are_checked(self):
        self.assertTrue(validate_bic("cobadeffxxx")["valid"])
        self.assertFalse(validate_bic("COBA-DE")["valid"])

        result = validate_payment_data(
            "DE89370400440532013000",
            "COBAFRPPXXX",
        )

        self.assertEqual(
            result["iban_bic_assignment"],
            "widerspruechlich",
        )
        self.assertFalse(result["valid_for_manual_confirmation"])

    def test_iban_is_masked_for_review_views(self):
        self.assertEqual(
            mask_iban("DE89370400440532013000"),
            "DE89 **** **** **** **30 00",
        )


class PlayerPaymentResultTests(unittest.TestCase):
    def test_only_players_with_positive_premiums_are_aggregated(self):
        result = eligible_premium_players(
            {
                "teams": [
                    {
                        "team_id": "herren_1",
                        "label": "Herren 1",
                        "players": [
                            {"name": "Max Mustermann", "premium_total": 10},
                            {"name": "Ohne Prämie", "premium_total": 0},
                        ],
                    },
                    {
                        "team_id": "herren_2",
                        "label": "Herren 2",
                        "players": [
                            {"name": "Max Mustermann", "premium_total": 5.5},
                        ],
                    },
                ]
            }
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["premium_total"], 15.5)
        self.assertEqual(len(result[0]["teams"]), 2)
        self.assertEqual(
            [team["premium_total"] for team in result[0]["teams"]],
            [10, 5.5],
        )

    def test_public_review_never_contains_full_iban_or_account_holder(self):
        full_iban = "DE89370400440532013000"
        review = _public_review(
            {
                "season": "2025/2026",
                "generated_at": "2026-06-13T12:00:00+00:00",
                "teams": [
                    {"team_id": "herren_1", "label": "Herren 1"},
                ],
                "players": [
                    {
                        "premium_name": "Max Mustermann",
                        "premium_total": 10,
                        "teams": [
                            {
                                "team_id": "herren_1",
                                "label": "Herren 1",
                                "premium_total": 10,
                            }
                        ],
                        "member_name": "Max Mustermann",
                        "match_quality": "exakt",
                        "match_score": 1,
                        "status": "eindeutig_gefunden",
                        "candidate_count": 1,
                        "account_holder": "Max Mustermann",
                        "validation": validate_payment_data(
                            full_iban,
                            "COBADEFFXXX",
                        ),
                    }
                ],
            }
        )
        serialized = json.dumps(review)

        self.assertNotIn(full_iban, serialized)
        self.assertNotIn("account_holder", serialized)
        self.assertIn("DE89 **** **** **** **30 00", serialized)
        self.assertTrue(review["manual_confirmation_required"])
        self.assertEqual(review["team_groups"][0]["team_id"], "herren_1")
        self.assertEqual(len(review["team_groups"][0]["players"]), 1)

    def test_manual_payment_only_exists_in_current_session(self):
        private_result = {
            "season": "2025/2026",
            "generated_at": "2026-06-13T12:00:00+00:00",
            "premium_generated_at": "2026-06-13T11:00:00+00:00",
            "teams": [{"team_id": "herren_1", "label": "Herren 1"}],
            "players": [
                {
                    "premium_name": "Max Mustermann",
                    "premium_total": 10,
                    "teams": [
                        {
                            "team_id": "herren_1",
                            "label": "Herren 1",
                            "premium_total": 10,
                        }
                    ],
                    "member_name": "",
                    "match_quality": "kein_treffer",
                    "match_score": 0,
                    "status": "nicht_gefunden",
                    "candidate_count": 0,
                    "account_holder": "",
                    "iban": "",
                    "bic": "",
                    "validation": validate_payment_data("", ""),
                }
            ],
        }
        full_iban = "DE89370400440532013000"
        clear_player_payment_session()
        _set_current_private_result(private_result)
        review = save_manual_player_payment(
            "Max Mustermann",
            {
                "account_holder": "Max Mustermann",
                "iban": full_iban,
                "bic": "COBADEFFXXX",
            },
        )
        current_review = load_current_player_payment_review()

        serialized_review = json.dumps(review)
        self.assertNotIn(full_iban, serialized_review)
        self.assertNotIn("account_holder", serialized_review)
        self.assertEqual(
            review["players"][0]["masked_iban"],
            "DE89 **** **** **** **30 00",
        )
        self.assertEqual(review["players"][0]["payment_source"], "manual")
        self.assertEqual(review["players"][0]["status"], "manuell_pruefen")
        self.assertEqual(current_review, review)

        clear_player_payment_session()

        self.assertIsNone(load_current_player_payment_review())

    def test_manual_payment_requires_fresh_dfbnet_run(self):
        clear_player_payment_session()

        with self.assertRaisesRegex(
            RuntimeError,
            "zuerst die Zahlungsdaten aktuell",
        ):
            save_manual_player_payment(
                "Max Mustermann",
                {
                    "account_holder": "Max Mustermann",
                    "iban": "DE89370400440532013000",
                    "bic": "COBADEFFXXX",
                },
            )

    def test_manual_offsets_are_subtracted_from_premiums(self):
        private_result = {
            "season": "2025/2026",
            "generated_at": "2026-06-13T12:00:00+00:00",
            "premium_generated_at": "2026-06-13T11:00:00+00:00",
            "teams": [{"team_id": "herren_1", "label": "Herren 1"}],
            "players": [
                {
                    "premium_name": "Max Mustermann",
                    "premium_total": 25,
                    "teams": [
                        {
                            "team_id": "herren_1",
                            "label": "Herren 1",
                            "premium_total": 25,
                        }
                    ],
                    "member_name": "Max Mustermann",
                    "match_quality": "exakt",
                    "match_score": 1,
                    "status": "eindeutig_gefunden",
                    "candidate_count": 1,
                    "account_holder": "Max Mustermann",
                    "iban": "DE89370400440532013000",
                    "bic": "COBADEFFXXX",
                    "validation": validate_payment_data(
                        "DE89370400440532013000",
                        "COBADEFFXXX",
                    ),
                }
            ],
        }
        clear_player_payment_session()
        _set_current_private_result(private_result)

        review = apply_player_payment_offsets(
            {
                "use_deckel": False,
                "manual_offsets": [
                    {
                        "premium_name": "Max Mustermann",
                        "label": "Trikot",
                        "amount": "-7,50",
                        "classification": {
                            "transaction_type": "Sonstige Gegenposition",
                            "top_category": "Test",
                            "sub_category": "Untertest",
                            "sphere": "Ideeller Bereich",
                        },
                    }
                ],
            }
        )

        player = review["players"][0]
        self.assertEqual(player["offset_total"], 7.5)
        self.assertEqual(player["final_amount"], 17.5)
        self.assertEqual(player["payment_direction"], "transfer")
        self.assertEqual(player["transaction_splits"][1]["amount"], -7.5)
        self.assertEqual(review["totals"]["offset_total"], 7.5)
        self.assertEqual(review["totals"]["transfer_total"], 17.5)

    def test_unassigned_deckel_positions_are_exported_as_debits(self):
        private_result = {
            "season": "2025/2026",
            "generated_at": "2026-06-13T12:00:00+00:00",
            "premium_generated_at": "2026-06-13T11:00:00+00:00",
            "teams": [],
            "players": [],
            "offset_configuration": {
                "deckel_path": "deckel.xlsx",
                "updated_at": "2026-06-13T12:00:00+00:00",
                "deckel_positions": [
                    {
                        "position_id": "deckel_1",
                        "raw_name": "Erika Beispiel",
                        "amount": 12.5,
                        "assignment_status": "unassigned",
                    }
                ],
            },
            "deckel_debtors": [
                {
                    "premium_name": "Erika Beispiel",
                    "deckel_position_ids": ["deckel_1"],
                    "deckel_amount_total": 12.5,
                    "member_name": "Erika Beispiel",
                    "match_quality": "exakt",
                    "match_score": 1,
                    "status": "eindeutig_gefunden",
                    "payment_source": "dfbnet",
                    "account_holder": "Erika Beispiel",
                    "iban": "DE89370400440532013000",
                    "bic": "COBADEFFXXX",
                    "validation": validate_payment_data(
                        "DE89370400440532013000",
                        "COBADEFFXXX",
                    ),
                }
            ],
        }
        clear_player_payment_session()
        _set_current_private_result(private_result)

        review = load_current_player_payment_review()
        export = export_player_payment_files({})

        self.assertEqual(review["totals"]["deckel_external_debit_total"], 12.5)
        self.assertEqual(review["totals"]["debit_total"], 12.5)
        self.assertEqual(export["exports"]["debit"]["count"], 1)
        self.assertEqual(export["exports"]["debit"]["total"], 12.5)


if __name__ == "__main__":
    unittest.main()
