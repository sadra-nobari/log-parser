import sys
import time
from pathlib import Path
from parser import parser
from statistics import Statistics
from formatter import print_report, export_json


def main() -> None:

    total_lines = 0
    malformed_lines = 0
    output_json = False

    args = [a for a in sys.argv[1:] if a != "--json"]
    if "--json" in sys.argv:
        output_json = True

    if not args:
        print("Usage: python main.py [--json] <path_to_log_file>")
        sys.exit(1)
    elif len(args) > 1:
        print("Error: Too many arguments provided.")
        print("Usage: python main.py [--json] <path_to_log_file>")
        sys.exit(1)

    log_file_path = Path(args[0])

    if not log_file_path.is_file():
        print(f"Error: File '{log_file_path}' does not exist.")
        sys.exit(1)

    print(f"Starting to process: {log_file_path.name}...\n")

    start = time.perf_counter()
    aggregator = Statistics()

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            total_lines += 1
            clean_line = line.strip()
            if not clean_line:
                continue

            try:
                log_entry = parser(clean_line)
                aggregator.entry_proc(log_entry)

            except ValueError:
                malformed_lines += 1
                continue

    if output_json:
        print(export_json(aggregator, malformed_lines))
    else:
        print_report(aggregator, malformed_lines)

    end = time.perf_counter()

    print(f"\nProcessing completed in {end - start:.2f} seconds.")


if __name__ == "__main__":
    main()
