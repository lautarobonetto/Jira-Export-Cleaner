import argparse
import sys

def parse_arguments():
    """
    Parses command-line arguments for the Jira Export Cleaner.
    """
    parser = argparse.ArgumentParser(
        description="Converts datetime columns in Jira CSV exports to a Google Spreadsheet compatible format."
    )

    parser.add_argument(
        "-i", "--input_file",
        required=True,
        help="Path to the source CSV file."
    )

    parser.add_argument(
        "-c", "--column_names",
        required=True,
        help="Comma-separated list of column names to convert (e.g., 'created,updated')."
    )

    parser.add_argument(
        "-o", "--output_file",
        required=True,
        help="Path where the processed CSV file will be saved."
    )

    parser.add_argument(
        "-l", "--log_file",
        required=False,
        help="Path to a log file for recording conversion details."
    )

    return parser.parse_args()

def main():
    """
    Main entry point for the script.
    """
    try:
        args = parse_arguments()
        print("Arguments parsed successfully:")
        print(f"  Input File: {args.input_file}")
        print(f"  Column Names: {args.column_names}")
        print(f"  Output File: {args.output_file}")
        if args.log_file:
            print(f"  Log File: {args.log_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
