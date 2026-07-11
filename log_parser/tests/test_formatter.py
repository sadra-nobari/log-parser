import json
import unittest
from log_parser.parser import LogEntry
from log_parser.statistics import Statistics
from log_parser.formatter import export_json


class TestFormatter(unittest.TestCase):

    def setUp(self):
        self.stats = Statistics()
        self.stats.entry_proc(LogEntry(
            ip="192.168.1.1",
            time="01/Jun/2026:14:05:30 +0000",
            method="GET",
            directory="/index",
            protocol="HTTP/1.1",
            status=200,
            bytes=1024,
            user_agent="Mozilla",
        ))
        self.stats.entry_proc(LogEntry(
            ip="10.0.0.1",
            time="01/Jun/2026:15:20:00 +0000",
            method="POST",
            directory="/index",
            protocol="HTTP/1.1",
            status=500,
            bytes=256,
            user_agent="curl/8.4.0",
        ))

    def test_export_json_structure(self):
        result = json.loads(export_json(self.stats, 2))
        self.assertEqual(result["total_requests"], 2)
        self.assertEqual(result["malformed_lines"], 2)
        self.assertEqual(result["unique_ips"], 2)
        self.assertEqual(result["total_errors"], 1)
        self.assertAlmostEqual(result["error_rate"], 50.0)
        self.assertEqual(len(result["top_endpoints"]), 1)
        self.assertEqual(len(result["top_ips"]), 2)
        self.assertEqual(len(result["hourly_traffic"]), 24)

    def test_export_json_empty(self):
        empty_stats = Statistics()
        result = json.loads(export_json(empty_stats, 0))
        self.assertEqual(result["total_requests"], 0)
        self.assertEqual(result["unique_ips"], 0)
        self.assertEqual(result["error_rate"], 0.0)
        self.assertEqual(result["top_endpoints"], [])
        self.assertEqual(result["top_ips"], [])

    def test_export_json_hourly_traffic_keys(self):
        result = json.loads(export_json(self.stats, 0))
        hours = list(result["hourly_traffic"].keys())
        self.assertEqual(hours, [f"{h:02d}" for h in range(24)])
        self.assertEqual(result["hourly_traffic"]["14"], 1)
        self.assertEqual(result["hourly_traffic"]["15"], 1)


if __name__ == "__main__":
    unittest.main()
