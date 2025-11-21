# Requirements for Jira Export Cleaner

## 1. Overview
The goal of this project is to provide a terminal-based Python utility that converts datetime columns in Jira CSV exports into a format compatible with Google Spreadsheets.

## 2. Input Specifications
- **Input File**: A CSV file containing Jira export data.
- **Target Columns**: A comma-separated list of column names to be processed (e.g., `created,updated`).
- **Date Format**: The input datetime strings are expected to follow the format: `dd/mmm/yy h:mm am/pm` (e.g., `05/Nov/25 5:16 PM`).

## 3. Functional Requirements

### 3.1. Command Line Interface (CLI)
The script must accept the following command-line arguments:
- `-i`, `--input_file` (Required): Path to the source CSV file.
- `-c`, `--column_names` (Required): Comma-separated string of column names to convert.
- `-o`, `--output_file` (Required): Path where the processed CSV file will be saved.
- `-l`, `--log_file` (Optional): Path to a log file for recording conversion details.

**Usage Example:**
```bash
python jira_export_cleaner.py -i input.csv -c "created,updated" -o output.csv -l process.log
```

### 3.2. Data Processing
- **Parsing**: The script must parse the datetime strings from the specified columns using the format `dd/mmm/yy h:mm am/pm`.
- **Conversion**: Successfully parsed dates must be converted to the ISO-like format `YYYY-MM-DD HH:mm:ss`.
- **Error Handling**: 
  - If a value in a target column does not match the expected format or cannot be parsed, the value in the output file must be set to the string `ERROR`.
  - The script must continue processing the remaining rows and columns even if errors are encountered.

### 3.3. Output Generation
- **CSV Output**: A new CSV file must be generated at the specified output path containing the converted data. All non-target columns must remain unchanged.
- **Logging**: 
  - If a log file path is provided, the script must write a log entry for each converted value.
  - **Log Format**: `File:<filename> Column:<col_name> original:<original_value> converted:<new_value> --> <status>`
  - **Status**: Should indicate `successful` for valid conversions.

## 4. Non-Functional Requirements
- **Language**: Python.
- **Environment**: The tool must run in a terminal environment.
- **Dependencies**: Standard library usage is preferred where possible, but external libraries (like `pandas`) may be used if necessary for CSV handling efficiency.
