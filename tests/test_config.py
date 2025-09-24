import os
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from managebac_checker.config import Config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path("./tmp_reports")
        self.env = {
            "MANAGEBAC_EMAIL": "student@example.com",
            "MANAGEBAC_PASSWORD": "secret",
            "REPORT_FORMAT": "console,html",
            "OUTPUT_DIR": str(self.output_dir),
        }

    def tearDown(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_loads_from_environment(self):
        with patch.dict(os.environ, self.env, clear=True):
            config = Config.from_environment()
            self.assertEqual(config.email, "student@example.com")
            self.assertEqual(config.password, "secret")
            self.assertIn("html", config.report_formats)
            self.assertTrue(config.output_dir.exists())

    def test_overrides_take_precedence(self):
        overrides = {"email": "override@example.com", "headless": False, "report_format": "json"}
        with patch.dict(os.environ, self.env, clear=True):
            config = Config.from_environment(overrides)
            self.assertEqual(config.email, "override@example.com")
            self.assertFalse(config.headless)
            self.assertEqual(config.report_formats, ["json"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
