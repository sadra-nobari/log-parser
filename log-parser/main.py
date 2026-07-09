import sys
from pathlib import Path

def main():
    

    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_log_file>")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Error: Too many arguments provided.")
        print("Usage: python main.py <path_to_log_file>")
        sys.exit(1)
        
           
    log_file_path = Path(sys.argv[1])
    

    if not log_file_path.is_file():
        print(f"Error: File '{log_file_path}' does not exist.")
        sys.exit(1)


    print(f"Starting to process: {log_file_path.name}...\n")

    print("--- Processing Completed ---")


if __name__ == "__main__":
    main()