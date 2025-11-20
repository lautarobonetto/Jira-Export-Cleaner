import argparse
import logging
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

def process_csv(input_file, output_file, column_names):
    """
    Reads the input CSV, processes it, and writes to the output CSV.
    
    Args:
        input_file (str): Path to the source CSV file.
        output_file (str): Path to the output CSV file.
        column_names (str): Comma-separated list of columns to convert.
    """
    target_columns = [col.strip() for col in column_names.split(',')]
    
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            if not fieldnames:
                logging.error("Input CSV file is empty or has no header.")
                return

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
                            
                            status = "successful" if new_value != "ERROR" else "failed"
                            log_msg = f"File:{input_file} Column:{col} original:{original_value} converted:{new_value} --> {status}"
                            logging.debug(log_msg)

                    writer.writerow(row)
            
        logging.info(f"Successfully processed '{input_file}' to '{output_file}'.")

    except FileNotFoundError:
        logging.error(f"Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
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
        nargs='+',
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
        
        # Configure logging
        # Configure logging
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File Handler
        if args.log_file:
            file_handler = logging.FileHandler(args.log_file, mode='w', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        column_names = " ".join(args.column_names)
        process_csv(args.input_file, args.output_file, column_names)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
