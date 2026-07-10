# Log-Parser tool using CLI

`Log-Parser` is a production-grade, zero-dependency command-line interface (CLI) tool designed to process and analyze massive web server access logs (Combined Log Format) efficiently. Built with memory-safety in mind, it utilizes a custom-built streaming architecture to parse gigabytes of log data line-by-line without overloading system memory.

---

## ✨ Features

*   **Memory-Efficient Streaming:** Reads and aggregates logs line-by-line. Memory footprint remains completely stable ($O(1)$ Space Complexity) whether processing a 10MB or 100GB file.
*   **Zero-Dependency Custom Parser:** No third-party parsing engines. Implements a high-performance, pre-compiled regular expression parser designed to handle "dirty" or interrupted real-world production logs seamlessly.
*   **Resilient Fault-Tolerance:** Malformed, corrupted, or incomplete lines are automatically skipped and counted without interrupting the core execution flow.
*   **Insightful Metrics Reporting:**
    *   Total requests & unique client IP counting.
    *   Top 10 highest-traffic endpoints (calculated efficiently via a Min-Heap implementation).
    *   Global error rates (4xx and 5xx status codes).
*   **Rich Terminal Visuals:** Generates an ASCII-based, self-scaling traffic distribution histogram across a 24-hour cycle to immediately pinpoint peak hours and traffic drops.

---

## 🏗️ Architecture & Data Flow

The project layout adheres strictly to clean code guidelines and separation of concerns:

```text
log-parser/
├── main.py          # Orchestrator, CLI argument parsing, and streaming file context
├── parser.py        # Custom parsing engine, LogEntry dataclass
├── statistics.py    # Metric calculation engine (In-memory aggregation via Hash Maps)
├── formatter.py     # Terminal visual rendering and ASCII Histogram layout
└── tests/
    └── test_parser.py # Isolated unit tests for edge-case inputs
```

## How to use

first you need to clone the project and open it on your terminal.

```bash
git clone https://github.com/sadra-nobari/log-parser.git
```
```bash
cd log-parser
```

and then run the program using this command

```bash
python3 log-parser/main.py ["path-to-the-log-file"]
```


## 🛠️ Technical Challenges & Solutions

During development, we encountered a couple of production-level challenges unique to parsing huge, real-world log files. Here is how they were solved:

### 1. The Tokenization Trap with `split(' ')`
*   **The Challenge:** Web server logs are space-delimited. However, critical fields like the `User-Agent` and `Request Line` containing the HTTP method and path also contain spaces inside their enclosing quotes (e.g., `"Mozilla/5.0 (Windows NT...)"`). A naive `.split(' ')` completely shatters these fields, making data aggregation impossible.
*   **The Solution:** We designed a precise, **pre-compiled Regular Expression Parser** (`re.compile`) using named capture groups. By defining rigid boundaries for quotes `""` and brackets `[]`, the parser safely isolates fields containing nested spaces in a single pass without breaking the token structure.
