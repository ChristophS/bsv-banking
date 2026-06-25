import tempfile
import unittest
from pathlib import Path

from banking_readonly.config import CredentialsConfig
from banking_readonly.credentials import CredentialError, load_credentials


def env_config(path: Path) -> CredentialsConfig:
    return CredentialsConfig(
        mode="env",
        env_file=path,
        username_variable="VOLKSBANK_USERNAME",
        password_variable="VOLKSBANK_PASSWORD",
        username_selector="#vrNetKey",
        password_selector="#pin",
        submit_selector="button[type='submit']",
    )


class CredentialTests(unittest.TestCase):
    def test_loads_credentials_without_interpolation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "banking.env"
            path.write_text(
                "VOLKSBANK_USERNAME=user-123\n"
                "VOLKSBANK_PASSWORD=pw-${NOT_EXPANDED}\n",
                encoding="utf-8",
            )

            credentials = load_credentials(env_config(path))

            self.assertEqual(credentials.username, "user-123")
            self.assertEqual(credentials.password, "pw-${NOT_EXPANDED}")
            self.assertNotIn("user-123", repr(credentials))
            self.assertNotIn("pw-", repr(credentials))

    def test_reports_missing_variable_without_other_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "banking.env"
            path.write_text(
                "VOLKSBANK_USERNAME=user-123\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                CredentialError, "VOLKSBANK_PASSWORD.*fehlt"
            ):
                load_credentials(env_config(path))


if __name__ == "__main__":
    unittest.main()
