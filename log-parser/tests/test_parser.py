import unittest
from parser import parser, LogEntry
from statistics import Statistics


class TestLogParser(unittest.TestCase):

    def test_parse_valid_line(self):

        valid_line = '171.90.27.4 - - [01/Jun/2026:00:00:00 +0000] "GET / HTTP/1.1" 301 8973 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"'
        result = parser(valid_line)

        # simple test
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

    def test_parse_line_with_dash_bytes(self):
        line_with_dash = '171.90.27.4 - - [01/Jun/2026:00:00:00 +0000] "GET / HTTP/1.1" 304 - "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"'
        result = parser(line_with_dash)
        self.assertEqual(result.status, 304)
        self.assertEqual(result.bytes, 0)


class TestStatistics(unittest.TestCase):

    def test_statistics_aggregation(self):
        stats = Statistics()

        # Create mock/actual LogEntry objects to process
        entry1 = LogEntry(
            ip="192.168.1.1",
            time="01/Jun/2026:14:05:30 +0000",
            method="GET",
            directory="/index",
            protocol="HTTP/1.1",
            status=200,
            bytes=1024,
            user_agent="Mozilla"
        )
        entry2 = LogEntry(
            ip="192.168.1.1",
            time="01/Jun/2026:14:15:30 +0000",
            method="GET",
            directory="/products",
            protocol="HTTP/1.1",
            status=404,
            bytes=512,
            user_agent="Mozilla"
        )
        entry3 = LogEntry(
            ip="10.0.0.1",
            time="01/Jun/2026:15:20:00 +0000",
            method="POST",
            directory="/index",
            protocol="HTTP/1.1",
            status=500,
            bytes=256,
            user_agent="Mozilla"
        )

        stats.entry_proc(entry1)
        stats.entry_proc(entry2)
        stats.entry_proc(entry3)

        self.assertEqual(stats.total_requests, 3)

        # Error code classification (404 and 500 should be errors)
        self.assertEqual(stats.total_errors[404], 1)
        self.assertEqual(stats.total_errors[500], 1)
        self.assertEqual(stats.total_pass[200], 1)
        self.assertEqual(sum(stats.total_errors.values()), 2)
        self.assertEqual(sum(stats.total_pass.values()), 1)

        # IP address tracking
        self.assertEqual(stats.ip_counts["192.168.1.1"], 2)
        self.assertEqual(stats.ip_counts["10.0.0.1"], 1)

        # Endpoint tracking
        self.assertEqual(stats.endpoint_counts["/index"], 2)
        self.assertEqual(stats.endpoint_counts["/products"], 1)

        # Hourly traffic tracking
        self.assertEqual(stats.hourly_traffic["14"], 2)
        self.assertEqual(stats.hourly_traffic["15"], 1)

        # Reporting
        self.assertEqual(stats.get_top_endpoints(limit=1), [("/index", 2)])
        self.assertEqual(stats.get_top_ips(limit=1), [("192.168.1.1", 2)])


if __name__ == "__main__":
    unittest.main()
