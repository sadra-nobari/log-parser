import re

log_pattern = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<directory>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d+)\s+'
    r'(?P<bytes>\d+)\s+'
    r'"[^"]*"\s+'
    r'"(?P<user_agent>[^"]+)"$'
)


def parser(line):
    match = log_pattern.match(line)
    if not match:
        raise ValueError("Malformed log line")