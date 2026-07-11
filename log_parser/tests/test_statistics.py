import unittest
from log_parser.parser import LogEntry
from log_parser.statistics import Statistics


class TestStatistics(unittest.TestCase):

    def setUp(self):
        self.stats = Statistics()
        self.entry1 = LogEntry(
            ip="192.168.1.1",
            time="01/Jun/2026:14:05:30 +0000",
            method="GET",
            directory="/index",
            protocol="HTTP/1.1",
            status=200,
            bytes=1024,
            user_agent="Mozilla",
        )
        self.entry2 = LogEntry(
            ip="192.168.1.1",
            time="01/Jun/2026:14:15:30 +0000",
            method="GET",
            directory="/products",
            protocol="HTTP/1.1",
            status=404,
            bytes=512,
            user_agent="Mozilla",
        )
        self.entry3 = LogEntry(
            ip="10.0.0.1",
            time="01/Jun/2026:15:20:00 +0000",
            method="POST",
            directory="/index",
            protocol="HTTP/1.1",
            status=500,
            bytes=256,
            user_agent="Mozilla",
        )

    def test_statistics_aggregation(self):
        self.stats.entry_proc(self.entry1)
        self.stats.entry_proc(self.entry2)
        self.stats.entry_proc(self.entry3)

        self.assertEqual(self.stats.total_requests, 3)

        self.assertEqual(self.stats.total_errors[404], 1)
        self.assertEqual(self.stats.total_errors[500], 1)
        self.assertEqual(self.stats.total_pass[200], 1)
        self.assertEqual(sum(self.stats.total_errors.values()), 2)
        self.assertEqual(sum(self.stats.total_pass.values()), 1)

        self.assertEqual(self.stats.ip_counts["192.168.1.1"], 2)
        self.assertEqual(self.stats.ip_counts["10.0.0.1"], 1)

        self.assertEqual(self.stats.endpoint_counts["/index"], 2)
        self.assertEqual(self.stats.endpoint_counts["/products"], 1)

        self.assertEqual(self.stats.hourly_traffic["14"], 2)
        self.assertEqual(self.stats.hourly_traffic["15"], 1)

        self.assertEqual(self.stats.get_top_endpoints(limit=1), [("/index", 2)])
        self.assertEqual(self.stats.get_top_ips(limit=1), [("192.168.1.1", 2)])

    def test_empty_statistics(self):
        self.assertEqual(self.stats.total_requests, 0)
        self.assertEqual(self.stats.get_top_endpoints(), [])
        self.assertEqual(self.stats.get_top_ips(), [])

    def test_error_rate(self):
        self.stats.entry_proc(self.entry1)
        self.stats.entry_proc(self.entry2)
        self.stats.entry_proc(self.entry3)

        total_errors = sum(self.stats.total_errors.values())
        self.assertEqual(total_errors, 2)
        self.assertEqual(self.stats.total_requests, 3)
        self.assertAlmostEqual(total_errors / self.stats.total_requests * 100, 66.666, places=2)


if __name__ == "__main__":
    unittest.main()
