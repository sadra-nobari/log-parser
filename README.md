# Log-Parser

CLI tool for parsing and analyzing web server access logs (Combined Log Format). No third-party dependencies. Streams input line-by-line so memory usage stays flat regardless of file size.

## Features

- Streaming line-by-line parser, constant memory usage independent of file size
- Regex-based parser (pre-compiled, named capture groups), no external parsing libraries
- Skips malformed/corrupted lines instead of failing, and reports how many were skipped
- Metrics: total requests, unique client IPs, top 10 endpoints by traffic, 4xx/5xx error rates
- ASCII histogram of request volume by hour
- Reports total processing time

## Project Layout

```text
log-parser/
├── main.py          # CLI entry point, argument parsing, file streaming
├── parser.py         # Log line parser, LogEntry dataclass
├── statistics.py      # Metric aggregation
├── formatter.py       # Terminal output and histogram rendering
└── tests/
    └── test_parser.py # Unit tests
```

## Usage

```bash
git clone https://github.com/sadra-nobari/log-parser.git
cd log-parser
python3 main.py <path-to-log-file>
```

## Testing

No test framework dependencies required.

```bash
python -m unittest discover -s tests
```

## Technical Challenges & Solutions

During development, we encountered a couple of production-level challenges unique to parsing huge, real-world log files. Here is how they were solved:

### 1. The Tokenization Trap with `split(' ')`
*   **The Challenge:** Web server logs are space-delimited. However, critical fields like the `User-Agent` and `Request Line` containing the HTTP method and path also contain spaces inside their enclosing quotes (e.g., `"Mozilla/5.0 (Windows NT...)"`). A naive `.split(' ')` completely shatters these fields, making data aggregation impossible.
*   **The Solution:** We designed a precise, **pre-compiled Regular Expression Parser** (`re.compile`) using named capture groups. By defining rigid boundaries for quotes `""` and brackets `[]`, the parser safely isolates fields containing nested spaces in a single pass without breaking the token structure.
