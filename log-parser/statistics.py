from collections import Counter
from parser import LogEntry
import re

date_pattern = re.compile(
    r"^\d{2}/\w+/\d{4}:(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}) [+-]\d{4}$"
)


class Statistics:
    def __init__(self):
        self.total_requests: int = 0
        self.total_errors: dict = Counter()
        self.total_pass: dict = Counter()
        self.ip_counts: dict = Counter()
        self.endpoint_counts: dict = Counter()
        self.hourly_traffic: dict = Counter()

    def entry_proc(self, entry: LogEntry) -> None:
        self.total_requests += 1

        # processing status codes
        if 400 <= entry.status < 600:
            self.total_errors[entry.status] += 1
        else:
            self.total_pass[entry.status] += 1

        # processing ip and endpoint counts
        self.ip_counter(entry.ip)
        self.endpoint_counter(entry.directory)
        self.traffic(entry.time)

    def ip_counter(self, ip: str) -> None:
        self.ip_counts[ip] += 1

    def endpoint_counter(self, endpoint: str) -> None:
        self.endpoint_counts[endpoint] += 1

    def traffic(self, time: str) -> None:
        # processing hourly traffic
        try:
            new_time = date_pattern.match(time)

            if new_time:
                hour = new_time.group("hour")
                self.hourly_traffic[hour] += 1
        except Exception as e:
            raise ValueError(f"Error processing time: {e}")

    def get_top_endpoints(self, limit: int = 10) -> list:
        return self.endpoint_counts.most_common(limit)

    def get_top_ips(self, limit: int = 10) -> list:
        return self.ip_counts.most_common(limit)

    def get_hourly_report(self) -> dict:
        return self.hourly_traffic
