import sys
import time
from pathlib import Path
from parser import parser
from statistics import Statistics
from formatter import print_report


def main():

    total_lines = 0
    malformed_lines = 0
    # if inputs are not provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_log_file>")
        sys.exit(1)

    # if too many inputs are provided
    elif len(sys.argv) > 2:
        print("Error: Too many arguments provided.")
        print("Usage: python main.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = Path(sys.argv[1])

    if not log_file_path.is_file():
        print(f"Error: File '{log_file_path}' does not exist.")
        sys.exit(1)

    print(f"Starting to process: {log_file_path.name}...\n")

    start = time.perf_counter()  # Start the timer
    aggregator = Statistics()  # Create an instance of the Statistics class
    # reading each line
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            total_lines += 1
            clean_line = line.strip()

            # if the line is empty, skip it
            if not clean_line:
                continue

            try:
                log_entry = parser(clean_line)
                aggregator.entry_proc(log_entry)

            except ValueError as e:
                malformed_lines += 1
                line_number = total_lines
                continue

    print_report(
        aggregator, malformed_lines
    )  # Call the print_report function with the aggregator instance

    end = time.perf_counter()  # End the timer

    print(f"\nProcessing completed in {end - start:.2f} seconds.")


if __name__ == "__main__":
    main()
