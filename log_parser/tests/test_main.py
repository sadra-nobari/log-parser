import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from log_parser.main import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_log = Path(__file__).resolve().parent.parent.parent / "access.log" / "test.log"

    @patch("builtins.print")
    def test_main_no_args(self, mock_print):
        with patch.object(sys, "argv", ["main.py"]):
            with self.assertRaises(SystemExit):
                main()

    @patch("builtins.print")
    def test_main_nonexistent_file(self, mock_print):
        with patch.object(sys, "argv", ["main.py", "/nonexistent.log"]):
            with self.assertRaises(SystemExit):
                main()

    @patch("builtins.print")
    def test_main_json_flag(self, mock_print):
        with patch.object(sys, "argv", ["main.py", "--json", str(self.test_log)]):
            main()
            args_list = [c[0][0] for c in mock_print.call_args_list]
            json_output = next((a for a in args_list if a.strip().startswith("{")), None)
            self.assertIsNotNone(json_output)
            data = json.loads(json_output)
            self.assertIn("total_requests", data)
            self.assertIn("malformed_lines", data)

    @patch("builtins.print")
    def test_main_runs_successfully(self, mock_print):
        with patch.object(sys, "argv", ["main.py", str(self.test_log)]):
            main()
            printed_text = " ".join(str(c[0][0]) for c in mock_print.call_args_list)
            self.assertIn("Processing completed", printed_text)


if __name__ == "__main__":
    unittest.main()
