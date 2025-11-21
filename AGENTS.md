# AGENTS.md - AI Assistant Guide for Jira Export Cleaner

## Project Overview

**Jira Export Cleaner** is a terminal-based Python utility that converts datetime columns in Jira CSV exports to a Google Spreadsheet-compatible format. The project was developed incrementally following a use-case-driven approach.

### Purpose
- **Primary Goal**: Convert Jira datetime columns from format `dd/mmm/yy h:mm am/pm` (e.g., `05/Nov/25 5:16 PM`) to ISO-like format `YYYY-MM-DD HH:mm:ss` (e.g., `2025-11-05 17:16:00`)
- **Use Case**: Enable easy import of Jira CSV exports into Google Spreadsheets with proper datetime formatting
- **Processing Model**: Single execution converts one or more specified datetime columns in a CSV file

---

## Project Structure

```
/Users/lautarobonetto/projects/Jira-Export-Cleaner/
├── jira_export_cleaner.py    # Main executable script
├── README.md                  # User-facing documentation
├── docs/
│   ├── requirements.md            # Detailed functional requirements
│   ├── use-cases.md               # Implementation roadmap (UC-1 through UC-6)
│   └── architecture.md            # Design philosophy and component breakdown
├── AGENTS.md                 # This file - AI assistant guide
└── .gitignore                # Git ignore configuration
```

### Key Files

#### `jira_export_cleaner.py` (157 lines)
The main executable script containing all functionality:
- **Functions**:
  - `convert_datetime(date_str, date_format)`: Core conversion logic
  - `process_csv(input_file, output_file, column_names, date_format)`: CSV processing engine
  - `parse_arguments()`: CLI argument parser using argparse
  - `main()`: Entry point with logging configuration

#### `README.md`
User-facing documentation with:
- Usage examples
- Parameter descriptions
- Input/output format specifications
- Example commands including custom date format usage

#### `docs/requirements.md`
Formal requirements document covering:
- CLI specifications
- Data processing requirements
- Error handling requirements
- Logging requirements

#### `docs/use-cases.md`
Development roadmap broken into 6 use cases:
- UC-1: CLI Initialization & Argument Parsing ✅ Completed
- UC-2: Core Date Conversion Logic ✅ Completed
- UC-3: CSV File I/O (Passthrough) ✅ Completed
- UC-4: Column Targeting & Transformation ✅ Completed
- UC-5: Error Handling & Resilience ✅ Completed
- UC-6: Logging ✅ Completed

#### `docs/architecture.md`
Technical design document explaining:
- Modular functional design philosophy
- Technology stack (Python 3.x standard library)
- Component breakdown
- Data flow diagram

---

## Current Implementation Status

### ✅ Completed Features

1. **CLI Argument Parsing** (UC-1)
   - Uses `argparse` for robust parsing
   - Required args: `-i` (input), `-c` (columns), `-o` (output)
   - Optional args: `-l` (log file), `-f` (date format)
   - Column names support: Handles space-separated arguments with `nargs='+'`

2. **Date Conversion Logic** (UC-2)
   - Configurable input date format (default: `%d/%b/%y %I:%M %p`)
   - Fixed output format: `%Y-%m-%d %H:%M:%S`
   - Returns "ERROR" string for unparseable dates

3. **CSV Processing** (UC-3, UC-4)
   - Uses `csv.DictReader` and `csv.DictWriter`
   - Preserves all non-target columns
   - Processes multiple columns in single execution
   - UTF-8 encoding support

4. **Error Handling** (UC-5)
   - Graceful handling of invalid dates (writes "ERROR")
   - Continues processing on individual conversion failures
   - Exits with appropriate error codes on critical failures

5. **Logging** (UC-6)
   - Dual logging: console (INFO level) + file (DEBUG level)
   - Uses Python's `logging` module
   - Console format: `%(levelname)s: %(message)s`
   - File format: `%(asctime)s - %(levelname)s - %(message)s`
   - Per-conversion logs: `File:{file} Column:{col} original:{orig} converted:{new} --> {status}`

### Recent Enhancements

1. **Configurable Date Formats** (Latest feature)
   - Added `--date_format` / `-f` parameter
   - Allows custom input date format strings
   - Default remains `%d/%b/%y %I:%M %p` for Jira compatibility

2. **Improved Logging Implementation**
   - Refactored from manual file handling to `logging` module
   - Separate handlers for console and file output
   - Proper log level control

3. **Robust Column Name Parsing**
   - Fixed issue with space-containing column names (e.g., "Last Viewed")
   - Changed from single string to `nargs='+'` for space-separated handling
   - Rejoins with spaces in processing: `column_names = " ".join(args.column_names)`

---

## Architecture Deep Dive

### Design Philosophy
**Modular Functional Design** - Avoids complex class hierarchies in favor of clean, separated functions. This keeps the script simple, readable, and maintainable.

### Technology Stack
- **Language**: Python 3.x
- **Dependencies**: Standard library only
  - `argparse`: CLI parsing
  - `csv`: File I/O
  - `datetime`: Date conversion
  - `logging`: Audit trail
  - `sys`: Exit codes and stdout

### Component Breakdown

```
┌─────────────────────────────────────────────┐
│                   main()                     │
│  • Parse arguments                           │
│  • Configure logging (console + file)       │
│  • Call process_csv()                        │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│             process_csv()                    │
│  • Open input/output CSV files              │
│  • Parse column names                        │
│  • Iterate rows                              │
│  • Call convert_datetime() per cell         │
│  • Log each conversion                       │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          convert_datetime()                  │
│  • Parse date string                         │
│  • Return formatted string or "ERROR"       │
└─────────────────────────────────────────────┘
```

### Data Flow

1. User executes: `python jira_export_cleaner.py -i input.csv -c created,updated -o output.csv`
2. `parse_arguments()` validates and parses CLI args
3. `main()` configures logging handlers
4. `process_csv()` opens input CSV
5. For each row:
   - Extract values from target columns
   - Call `convert_datetime()` for each
   - Update row dictionary
   - Log conversion result
   - Write modified row to output
6. Close files and exit

---

## Code Patterns and Important Details

### Column Name Parsing (Lines 96-97, 148)
```python
# Argument parsing supports space-separated multi-word column names
parser.add_argument("-c", "--column_names", required=True, nargs='+', ...)

# Rejoined in main before passing to process_csv
column_names = " ".join(args.column_names)
```

**Context**: This was implemented to handle column names with spaces like "Last Viewed". The `nargs='+'` captures space-separated words, and they're rejoined before processing.

### Dual Logging Configuration (Lines 128-146)
```python
# Root logger at DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console: INFO level, simple format
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')

# File: DEBUG level, timestamped format
file_handler = logging.FileHandler(args.log_file, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
```

**Context**: This allows detailed debugging logs in the file while keeping console output clean.

### Error-Resilient Conversion (Lines 52-66)
```python
for row in reader:
    for col in target_columns:
        if col in row:
            original_value = row[col]
            new_value = original_value
            try:
                new_value = convert_datetime(original_value, date_format)
                row[col] = new_value
            except Exception:
                row[col] = "ERROR"
                new_value = "ERROR"
            
            status = "successful" if new_value != "ERROR" else "failed"
            log_msg = f"File:{input_file} Column:{col} original:{original_value} converted:{new_value} --> {status}"
            logging.debug(log_msg)
```

**Context**: Individual conversion failures don't stop processing. Each failure results in "ERROR" in the output cell.

### Date Format Handling (Lines 7-25)
```python
def convert_datetime(date_str, date_format="%d/%b/%y %I:%M %p"):
    try:
        dt = datetime.strptime(date_str, date_format)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "ERROR"
```

**Context**: Input format is configurable, output format is fixed to `YYYY-MM-DD HH:mm:ss` for Google Sheets compatibility.

---

## Development History

### Conversation Timeline

1. **Create Requirements Document** (Conv: 557ad017)
   - Created `requirements.md` from README analysis
   - Established formal requirements

2. **Implement UC-1: CLI Parsing** (Conv: c5df2599)
   - Set up `argparse`
   - Implemented basic CLI structure
   - Validated argument parsing

3. **Fixing CSV Datetime Conversion** (Conv: 3cea9f6d)
   - Fixed column name parsing for spaces
   - Implemented standard logging module
   - Replaced manual log handling

4. **Refine Logging Implementation** (Conv: 9e1b7629)
   - Enhanced log formatting
   - Dual output (console + file)
   - Proper log levels

5. **Configurable Date Formats** (Conv: 67c5e650)
   - Added `--date_format` parameter
   - Made input format configurable
   - Updated documentation

### Evolution Notes
- Started with basic requirements gathering
- Followed use-case-driven development (UC-1 through UC-6)
- Iteratively refined based on real-world issues (e.g., space in column names)
- Enhanced logging capabilities progressively
- Added configurability while maintaining sensible defaults

---

## Common Tasks and Modifications

### Adding a New CLI Argument

1. Add to `parse_arguments()` function:
```python
parser.add_argument(
    "-x", "--new_arg",
    required=False,
    default="default_value",
    help="Description of the new argument"
)
```

2. Access in `main()`: `args.new_arg`

3. Pass to `process_csv()` if needed

4. Update README.md with new parameter

### Modifying Output Format

**Current**: Output format is hardcoded to `%Y-%m-%d %H:%M:%S`

**To make configurable**:
1. Add `--output_date_format` argument in `parse_arguments()`
2. Modify `convert_datetime()` to accept `output_format` parameter
3. Replace `return dt.strftime("%Y-%m-%d %H:%M:%S")` with user-provided format

### Adding Support for Multiple Input Date Formats

**Current**: Single format per execution

**To support auto-detection**:
1. Define list of common formats
2. Modify `convert_datetime()` to try each format
3. Return first successful parse or "ERROR"

Example:
```python
def convert_datetime(date_str, date_formats=None):
    if date_formats is None:
        date_formats = ["%d/%b/%y %I:%M %p", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
    
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return "ERROR"
```

### Handling Time Zones

**Current**: No timezone support (naive datetime)

**To add timezone support**:
1. Import `from datetime import timezone`
2. Modify `convert_datetime()` to handle timezone-aware strings
3. Consider adding `--timezone` CLI argument
4. Use `datetime.strptime().replace(tzinfo=...)` or `astimezone()`

---

## Testing Approach

### Manual Testing Pattern

The project was developed with manual testing. Common test scenarios:

1. **Basic Conversion**:
```bash
python jira_export_cleaner.py -i test_input.csv -c created -o test_output.csv -l test.log
```

2. **Multiple Columns**:
```bash
python jira_export_cleaner.py -i input.csv -c created,updated,"Last Viewed" -o output.csv
```

3. **Custom Date Format**:
```bash
python jira_export_cleaner.py -i input.csv -c timestamp -o output.csv -f "%Y-%m-%d %H:%M:%S"
```

4. **Error Handling**:
- Test with non-existent input file
- Test with invalid date values in CSV
- Test with non-existent column names

### Future Testing Improvements

Consider adding:
- Unit tests for `convert_datetime()`
- Integration tests with sample CSV files
- Edge case tests (empty files, missing headers, special characters)
- Performance tests with large files

---

## Troubleshooting Guide

### Common Issues

#### Issue: "Column not found" errors
**Cause**: Column name mismatch (case-sensitive, whitespace)
**Solution**: Check exact column name in CSV header, use quotes for multi-word names

#### Issue: All dates convert to "ERROR"
**Cause**: Input format mismatch
**Solution**: Verify actual date format in CSV, specify with `-f` parameter

#### Issue: Log file not created
**Cause**: Missing `-l` parameter or permission issues
**Solution**: Ensure `-l` is provided and directory is writable

#### Issue: Output file is empty
**Cause**: Input file not found or permission denied
**Solution**: Check input file path and read permissions

---

## Best Practices for AI Assistants

### When Modifying This Project

1. **Maintain Backward Compatibility**: Existing scripts depend on current CLI interface
2. **Update All Documentation**: Keep README.md, requirements.md, and architecture.md in sync
3. **Follow Functional Design**: Avoid adding classes unless absolutely necessary
4. **Preserve Error Resilience**: Never let individual conversion failures crash the process
5. **Test with Real Jira Exports**: Jira CSV format can be quirky
6. **Keep Dependencies Minimal**: Prefer standard library over external packages

### When Debugging

1. **Check Log Files**: DEBUG level logs show every conversion attempt
2. **Verify CSV Structure**: Use `csv.DictReader` to inspect headers
3. **Test Date Format**: Isolate `convert_datetime()` with sample strings
4. **Review argparse Output**: Print `vars(args)` to see parsed arguments

### When Adding Features

1. **Create New Use Case**: Follow UC-1 through UC-6 pattern
2. **Update architecture.md**: Document design decisions
3. **Write Examples**: Add to README.md with concrete examples
4. **Consider Error Cases**: What happens when this feature fails?

---

## Example Workflows

### Workflow 1: Processing a Jira Export

```bash
# 1. Export CSV from Jira with datetime columns

# 2. Identify datetime columns (e.g., "created", "updated", "Last Viewed")

# 3. Run converter
python jira_export_cleaner.py \
  -i jira_export_2024.csv \
  -c created,updated,"Last Viewed" \
  -o jira_export_cleaned.csv \
  -l conversion.log

# 4. Review log for any errors
cat conversion.log | grep failed

# 5. Import cleaned CSV into Google Sheets
```

### Workflow 2: Handling Custom Date Formats

```bash
# If Jira export has format: "2024-11-05 17:16:00"
python jira_export_cleaner.py \
  -i input.csv \
  -c timestamp \
  -o output.csv \
  -f "%Y-%m-%d %H:%M:%S"
```

### Workflow 3: Debugging Conversion Issues

```bash
# 1. Run with logging enabled
python jira_export_cleaner.py -i input.csv -c created -o output.csv -l debug.log

# 2. Check for failed conversions
grep "failed" debug.log

# 3. Examine original values that failed
grep "ERROR" output.csv

# 4. Adjust date format or fix source data
```

---

## Future Enhancement Ideas

### Potential Features (Not Yet Implemented)

1. **Batch Processing**: Process multiple CSV files in one execution
2. **Configuration Files**: Load settings from `.ini` or `.yaml` file
3. **Dry Run Mode**: Preview changes without writing output
4. **Statistics Report**: Summary of successful/failed conversions
5. **Column Auto-Detection**: Automatically identify datetime columns
6. **GUI Interface**: Simple Tkinter interface for non-technical users
7. **Pandas Integration**: Option to use pandas for performance on large files
8. **Timezone Conversion**: Support for timezone-aware datetime conversion
9. **Custom Error Values**: Allow user to specify alternative to "ERROR"
10. **Validation Mode**: Check if all dates are valid before converting

---

## Contact and Maintenance

**Project Owner**: Lautaro Bonetto  
**Project Path**: `/Users/lautarobonetto/projects/Jira-Export-Cleaner`  
**Initial Development**: November 2024  
**Current Status**: Production-ready, all use cases implemented

### For AI Assistants

When working on this project:
- Respect the existing functional design pattern
- Test changes with realistic Jira CSV data
- Update all documentation files when making significant changes
- Follow the use-case-driven development approach
- Keep the script lightweight and dependency-free

---

## Quick Reference

### CLI Syntax
```bash
python jira_export_cleaner.py -i <input> -c <columns> -o <output> [-l <log>] [-f <format>]
```

### Default Date Format
- **Input**: `%d/%b/%y %I:%M %p` (e.g., `05/Nov/25 5:16 PM`)
- **Output**: `%Y-%m-%d %H:%M:%S` (e.g., `2025-11-05 17:16:00`)

### Exit Codes
- `0`: Success
- `1`: Error (file not found, processing failure, etc.)

### Log Format
```
File:<filename> Column:<column> original:<value> converted:<value> --> <status>
```

---

**Last Updated**: 2025-11-20  
**Document Version**: 1.0  
**AI Agent**: Antigravity by Google Deepmind
