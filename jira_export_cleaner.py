import argparse
import sys
import csv
from datetime import datetime

def convert_datetime(date_str):
    """
    Converts a Jira datetime string to a Google Spreadsheet compatible format.
    
    Args:
        date_str (str): The date string to convert (e.g., '05/Nov/25 5:16 PM').
        
    Returns:
        str: The converted date string in 'YYYY-MM-DD HH:mm:ss' format,
             or 'ERROR' if parsing fails.
    """
    try:
        # Parse the date string
        dt = datetime.strptime(date_str, "%d/%b/%y %I:%M %p")
        # Format to ISO-like format
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "ERROR"

def process_csv(input_file, output_file, column_names, log_file=None):
    """
    Reads the input CSV, processes it, and writes to the output CSV.
    
    Args:
        input_file (str): Path to the source CSV file.
        output_file (str): Path to the output CSV file.
        column_names (str): Comma-separated list of columns to convert.
        log_file (str, optional): Path to the log file.
    """
    target_columns = [col.strip() for col in column_names.split(',')]
    
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            if not fieldnames:
                print("Error: Input CSV file is empty or has no header.", file=sys.stderr)
                return

            # Open log file if provided
            log_handle = None
            if log_file:
                try:
                    log_handle = open(log_file, 'w', encoding='utf-8')
                except Exception as e:
                    print(f"Warning: Could not open log file '{log_file}': {e}", file=sys.stderr)

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in reader:
                    for col in target_columns:
                        if col in row:
                            original_value = row[col]
                            new_value = original_value
                            try:
                                new_value = convert_datetime(original_value)
                                row[col] = new_value
                            except Exception:
                                row[col] = "ERROR"
                                new_value = "ERROR"
                            
                            if log_handle:
                                status = "successful" if new_value != "ERROR" else "failed"
                                log_msg = f"File:{input_file} Column:{col} original:{original_value} converted:{new_value} --> {status}\n"
                                log_handle.write(log_msg)

                    writer.writerow(row)
            
            if log_handle:
                log_handle.close()
                    
        print(f"Successfully processed '{input_file}' to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during processing: {e}", file=sys.stderr)
        sys.exit(1)

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
        process_csv(args.input_file, args.output_file, args.column_names, args.log_file)
        
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
