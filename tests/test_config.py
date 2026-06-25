import tempfile
import unittest
from pathlib import Path

from banking_readonly.config import ConfigError, load_config


VALID_CONFIG = """
[bank]
login_url = "https://bank.test/login"

[detection]
success_selector = "main[data-testid='overview']"
success_url_pattern = '^https://bank\\.test/overview'
timeout_seconds = 60
poll_interval_seconds = 0.25
stable_seconds = 1.0

[runtime]
profile_dir = ".runtime/profile"
log_dir = ".runtime/logs"
screenshot_dir = ".runtime/screenshots"
navigation_timeout_seconds = 30
"""

SPARKASSE_CONFIG = """
[bank]
provider = "sparkasse"
login_url = "https://www.sparkasse-gm.de/de/home.html"

[credentials]
mode = "env"
env_file = "banking.env"
username_variable = "SPARKASSE_USERNAME"
password_variable = "SPARKASSE_PASSWORD"

[export]
format = "Excel (CSV-MT940)"
period = "CURRENT_VIEW"
output_dir = ".runtime/exports/sparkasse"

[[accounts]]
name = "Sichteinlagen"
iban = "DE29 3845 0000 0000 3592 32"
filename = "veranstaltungen.csv"

[[accounts]]
name = "Sichteinlagen - Abt. Jugendfussball"
iban = "DE71 3845 0000 0000 8164 13"
filename = "jugend.csv"

[[accounts]]
name = "Sichteinlagen - Vereinsheim"
iban = "DE85 3845 0000 0001 0135 56"
filename = "vereinsheim.csv"

[detection]
success_text_pattern = 'DE29\\s*3845\\s*0000\\s*0000\\s*3592\\s*32'

[runtime]
profile_dir = ".runtime/profile"
log_dir = ".runtime/logs"
screenshot_dir = ".runtime/screenshots"
"""


class ConfigTests(unittest.TestCase):
    def test_loads_valid_config_and_resolves_runtime_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            path.write_text(VALID_CONFIG, encoding="utf-8")

            config = load_config(path)

            self.assertEqual(config.login_url, "https://bank.test/login")
            self.assertEqual(config.detection.timeout_seconds, 60)
            self.assertEqual(config.export.format, "CSV")
            self.assertEqual(config.export.period, "FROM_SEARCH")
            self.assertEqual(
                config.runtime.log_dir, Path(temp_dir).resolve() / ".runtime/logs"
            )

    def test_rejects_credentials_in_url(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            path.write_text(
                VALID_CONFIG.replace(
                    "https://bank.test/login",
                    "https://user:secret@bank.test/login",
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ConfigError, "keine Zugangsdaten"):
                load_config(path)

    def test_requires_a_success_criterion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            without_criteria = VALID_CONFIG.replace(
                "success_selector = \"main[data-testid='overview']\"",
                'success_selector = ""',
            ).replace(
                "success_url_pattern = '^https://bank\\.test/overview'",
                'success_url_pattern = ""',
            )
            path.write_text(without_criteria, encoding="utf-8")

            with self.assertRaisesRegex(ConfigError, "Mindestens"):
                load_config(path)

    def test_rejects_other_export_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            path.write_text(
                VALID_CONFIG + '\n[export]\nformat = "PDF"\n',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ConfigError, "CSV"):
                load_config(path)

    def test_loads_sparkasse_accounts_and_two_step_login_defaults(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            path.write_text(SPARKASSE_CONFIG, encoding="utf-8")

            config = load_config(path)

            self.assertEqual(config.provider, "sparkasse")
            self.assertEqual(config.export.format, "CSV_MT940")
            self.assertEqual(config.export.period, "CURRENT_VIEW")
            self.assertEqual(
                [account.iban for account in config.export.accounts],
                [
                    "DE29384500000000359232",
                    "DE71384500000000816413",
                    "DE85384500000001013556",
                ],
            )
            self.assertEqual(
                config.credentials.username_submit_selector,
                (
                    "input[type='submit'][title='Weiter']:visible, "
                    "input[type='submit'][value='Weiter']:visible"
                ),
            )
            self.assertEqual(
                config.credentials.submit_selector,
                (
                    "input[type='submit'][title='Anmelden']:visible, "
                    "input[type='submit'][value='Anmelden']:visible, "
                    "button[type='submit']:visible"
                ),
            )

    def test_sparkasse_requires_account_allowlist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.toml"
            without_accounts = SPARKASSE_CONFIG.split("[[accounts]]", 1)[0]
            without_accounts += """
[detection]
success_text_pattern = "Konto"

[runtime]
profile_dir = ".runtime/profile"
log_dir = ".runtime/logs"
screenshot_dir = ".runtime/screenshots"
"""
            path.write_text(without_accounts, encoding="utf-8")

            with self.assertRaisesRegex(ConfigError, "mindestens ein"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
