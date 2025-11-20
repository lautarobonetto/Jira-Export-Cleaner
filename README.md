# Jira-Export-Cleaner
This is terminal based python project. The project goal is to convert Jira CVS datetime columns to a Google Spreadsheet compatible format.

Each time you execute this script, it will convert one datetime column at the time. This script will recive as input the CSV file and the column name to convert. The outpur will be other CVS file with the converted datetime column. The script will also create a log file with the conversion results.

## Input format:
This script expects the CSV file to have datetime columns. By default, it expects the format: `dd/mmm/yy h:mm am/pm` (e.g., `05/Nov/25 5:16 PM`).

Example: `05/Nov/25 5:16 PM`

## Output format
This script will convert to the following format: `YYYY-MM-DD HH:mm:ss`. In case of error, the column value will be the string `ERROR`.

Example: `2025-11-05 17:16:00`

You can specify a custom format using the `--date_format` argument.

## Parameters
- -i, --input_file <input_file> : Input CSV file (String format).
- -c, --column_names <column_names> : Column names to convert (Comma-separated String format).
- -o, --output_file <output_file> : Output CSV file (String format).
- -l, --log_file <log_file> : Log file (String format) (Optional).
- -f, --date_format <date_format> : Format of the input date string (String format) (Optional, default: `%d/%b/%y %I:%M %p`).

## Usage
```bash
python jira_export_cleaner.py -i <input_file> -c <column_names> -o <output_file> [-l <log_file>] [-f <date_format>]
```

## Example
```bash
python jira_export_cleaner.py -i jira_export.csv -c created,updated -o jira_export_cleaned.csv -l jira_export_cleaned.log
```

### Custom Date Format Example
```bash
python jira_export_cleaner.py -i input.csv -c "Last Viewed" -o output.csv -f "%Y-%m-%d %H:%M:%S"
```

## Output
```csv
issue_key,summary,created,updated
JIRA-1,Issue 1,2025-11-05 17:16:00,2025-11-05 17:16:00
JIRA-2,Issue 2,2025-11-05 17:16:00,2025-11-05 17:16:00
```

## Log file
```log
File:jira_export.csv Column:created original:05/Nov/25 5:16 PM converted:2025-11-05 17:16:00 --> successful
File:jira_export.csv Column:updated original:05/Nov/25 5:16 PM converted:2025-11-05 17:16:00 --> successful
```
