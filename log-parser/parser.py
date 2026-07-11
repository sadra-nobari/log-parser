import re
from dataclasses import dataclass

# regex for common log format; used to validate and extract fields
log_pattern = re.compile(
    r"^(?P<ip>\S+)\s+\S+\s+\S+\s+"
    r"\[(?P<time>[^\]]+)\]\s+"
    r'"(?P<method>\S+)\s+(?P<directory>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r"(?P<status>\d+)\s+"
    r"(?P<bytes>\d+|-)\s+"
    r'"[^"]*"\s+'
    r'"(?P<user_agent>[^"]+)"$'
)


@dataclass
class LogEntry:
    ip: str
    time: str
    method: str
    directory: str
    protocol: str
    status: int
    bytes: int
    user_agent: str


def parser(line: str):
    match = log_pattern.match(line)
    if not match:
        raise ValueError("Malformed log line")

    data = match.groupdict()

    # build LogEntry from regex groups
    try:
        return LogEntry(
            ip=data["ip"],
            time=data["time"],
            method=data["method"],
            directory=data["directory"],
            protocol=data["protocol"],
            status=int(data["status"]),
            bytes=int(data["bytes"]) if data["bytes"] != "-" else 0,
            user_agent=data["user_agent"],
        )
    except Exception:
        raise ValueError()
