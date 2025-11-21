# Architecture Design for Jira Export Cleaner

## 1. Design Philosophy
The solution will follow a **Modular Functional Design**. Given the requirement for a terminal-based utility and the goal of simplicity, we will avoid complex class hierarchies in favor of clean, separated functions handled by a main controller. This ensures the script is easy to read, maintain, and test.

## 2. Technology Stack

### 2.1. Language
- **Python 3.x**: Chosen for its strong support for text processing and wide availability.

### 2.2. Libraries
To minimize external dependencies and ensure portability, we will primarily use Python's **Standard Library**.

- **`argparse`**: For robust command-line argument parsing, help message generation, and validation.
- **`csv`**: For reading and writing CSV files. This is preferred over `pandas` for this specific use case to keep the tool lightweight and avoid heavy dependencies, as we are performing row-by-row transformations rather than complex data analysis.
- **`datetime`**: For parsing the source date strings and formatting them to the target ISO-like format.
- **`logging`** (or simple file I/O): For generating the conversion log file.

## 3. System Components

The application will be structured into logical components:

### 3.1. CLI Interface (`main`)
- **Responsibility**: Entry point of the application.
- **Actions**:
    1. Initialize the Argument Parser.
    2. Validate input file existence.
    3. Call the Processing Engine.
    4. Handle top-level exceptions and exit codes.

### 3.2. Argument Parser
- **Responsibility**: Define and parse command-line arguments (`-i`, `-c`, `-o`, `-l`).
- **Output**: A configuration object or dictionary containing the user's settings.

### 3.3. Processing Engine (`process_csv`)
- **Responsibility**: Orchestrate the reading, converting, and writing process.
- **Logic**:
    1. Open the input CSV file for reading.
    2. Open the output CSV file for writing.
    3. Identify the indices of the columns to be converted based on the header.
    4. Iterate through the input rows.
    5. For each row, apply the **Date Converter** to the target columns.
    6. Write the processed row to the output file.
    7. If logging is enabled, write the result to the log.

### 3.4. Date Converter (`convert_datetime`)
- **Responsibility**: Pure function to transform a single date string.
- **Input**: Date string (e.g., `05/Nov/25 5:16 PM`).
- **Output**: Tuple `(converted_date_string, status)`.
- **Logic**:
    - Attempt to parse using format `%d/%b/%y %I:%M %p`.
    - If successful, format to `%Y-%m-%d %H:%M:%S`.
    - If parsing fails, return `ERROR` and status `failed`.

### 3.5. Logger
- **Responsibility**: Write conversion details to the specified log file.
- **Format**: `File:<filename> Column:<col_name> original:<val> converted:<val> --> <status>`

## 4. Data Flow

1. **User** executes command.
2. **CLI** parses args.
3. **Engine** reads `input.csv` header.
4. **Engine** finds target column indices.
5. **Loop** over rows:
    - Extract value.
    - **Converter** transforms value.
    - **Engine** updates row data.
    - **Engine** writes to `output.csv`.
    - **Logger** appends to `log_file`.
6. **Exit**.
