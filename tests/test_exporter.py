import logging
import tempfile
import unittest
from pathlib import Path

from banking_readonly.exporter import (
    ALLOWED_ACCOUNTS,
    AllowedAccount,
    ExportError,
    _remove_partial_run,
    extract_sparkasse_account_balance,
    extract_volksbank_account_balance,
    normalize_iban,
    unique_matching_index,
)


class ExporterTests(unittest.TestCase):
    def test_allowlist_contains_exactly_the_four_approved_accounts(self):
        self.assertEqual(
            [(account.name, account.iban) for account in ALLOWED_ACCOUNTS],
            [
                ("Hauptkonto", "DE31384621350101206017"),
                ("Rücklagen", "DE09384621350101206025"),
                ("Ausstattung", "DE98384621350103038014"),
                ("Sparkonto", "DE25384621350101206416"),
            ],
        )

    def test_normalizes_formatted_iban(self):
        self.assertEqual(
            normalize_iban("DE31 3846 2135 0101 2060 17"),
            "DE31384621350101206017",
        )

    def test_finds_only_matching_name_and_full_iban(self):
        account = ALLOWED_ACCOUNTS[0]
        texts = [
            "Hauptkonto DE00 0000 0000 0000 0000 00",
            "Hauptkonto DE31 3846 2135 0101 2060 17",
            "Anderes Konto DE31 3846 2135 0101 2060 17",
        ]

        self.assertEqual(unique_matching_index(texts, account), 1)

    def test_rejects_duplicate_matches(self):
        account = AllowedAccount(
            "Hauptkonto", "DE31384621350101206017", "hauptkonto.csv"
        )
        text = "Hauptkonto DE31 3846 2135 0101 2060 17"

        with self.assertRaisesRegex(ExportError, "2-mal"):
            unique_matching_index([text, text], account)

    def test_removes_only_current_partial_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "exports"
            run_dir = output_dir / "run"
            run_dir.mkdir(parents=True)
            (run_dir / "partial.csv").write_bytes(b"partial")

            _remove_partial_run(run_dir, output_dir, logging.getLogger("test"))

            self.assertFalse(run_dir.exists())
            self.assertTrue(output_dir.exists())

    def test_extracts_labeled_sparkasse_balance_not_available_amount(self):
        balance, currency = extract_sparkasse_account_balance(
            "Sichteinlagen Kontostand -1.234,56 EUR "
            "Verfuegbar 2.000,00 EUR",
            "Sichteinlagen",
        )

        self.assertEqual(format(balance, ".2f"), "-1234.56")
        self.assertEqual(currency, "EUR")

    def test_rejects_ambiguous_unlabeled_sparkasse_amounts(self):
        with self.assertRaises(ExportError):
            extract_sparkasse_account_balance(
                "Sichteinlagen 1.234,56 EUR 2.000,00 EUR",
                "Sichteinlagen",
            )

    def test_extracts_labeled_volksbank_balance(self):
        balance, currency = extract_volksbank_account_balance(
            "Sparkonto DE25 3846 2135 0101 2064 16 "
            "Kontostand 5.000,00 EUR Verfuegbar 4.900,00 EUR",
            "Sparkonto",
        )

        self.assertEqual(format(balance, ".2f"), "5000.00")
        self.assertEqual(currency, "EUR")


if __name__ == "__main__":
    unittest.main()
