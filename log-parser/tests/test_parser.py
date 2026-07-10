import unittest
from parser import parser, LogEntry
class TestLogParser(unittest.TestCase):

    def test_parse_valid_line(self):

        valid_line = '171.90.27.4 - - [01/Jun/2026:00:00:00 +0000] "GET / HTTP/1.1" 301 8973 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"'
        result = parser(valid_line)

        #simple test
        self.assertIsInstance(result, LogEntry)
        self.assertEqual(result.ip, "171.90.27.4")
        self.assertEqual(result.method, "GET")
        self.assertEqual(result.directory, "/")
        self.assertEqual(result.status, 301)
        self.assertEqual(result.bytes, 8973)
        self.assertEqual(result.time, "01/Jun/2026:00:00:00 +0000")
        self.assertIn("Mozilla", result.user_agent)


    def test_parse_malformed_line_raises_exception(self):
        bad_line = "this is just a random broken text, not a log line at all"
        
        with self.assertRaises(ValueError):
            parser(bad_line)


if __name__ == '__main__':
    unittest.main()