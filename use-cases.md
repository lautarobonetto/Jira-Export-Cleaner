# Use Cases & Implementation Steps

This document outlines the use cases that will serve as the implementation roadmap. Each use case represents a distinct piece of functionality that can be implemented and verified incrementally.

## UC-1: CLI Initialization & Argument Parsing
**Goal**: Ensure the script can be called from the terminal and correctly parses the required and optional arguments.
- **Input**: `python jira_export_cleaner.py -i input.csv -c "created" -o output.csv`
- **Expected Behavior**:
    - The script starts without syntax errors.
    - It prints the parsed arguments to the console (temporary debug step).
    - It handles missing required arguments by showing the help message.
- **Implementation Focus**: `argparse` setup.

## UC-2: Core Date Conversion Logic
**Goal**: Implement and verify the function responsible for transforming the date strings.
- **Input**: String `05/Nov/25 5:16 PM`
- **Expected Output**: String `2025-11-05 17:16:00`
- **Input**: String `Invalid Date`
- **Expected Output**: String `ERROR`
- **Implementation Focus**: `datetime` parsing and formatting function.

## UC-3: CSV File I/O (Passthrough)
**Goal**: Establish the pipeline for reading the input CSV and creating the output CSV.
- **Input**: A valid CSV file.
- **Expected Behavior**:
    - The script reads the input file.
    - The script creates the output file.
    - The output file is an exact copy of the input file (initially).
- **Implementation Focus**: `csv` module `DictReader` and `DictWriter`.

## UC-4: Column Targeting & Transformation
**Goal**: Integrate the date conversion logic into the CSV processing loop.
- **Input**: CSV file with a `created` column containing `05/Nov/25 5:16 PM`.
- **Expected Behavior**:
    - The script identifies the `created` column based on the `-c` argument.
    - The output CSV contains `2025-11-05 17:16:00` in the `created` column.
    - Other columns remain untouched.
- **Implementation Focus**: Iterating rows and modifying specific dictionary keys.

## UC-5: Error Handling & Resilience
**Goal**: Ensure the process doesn't crash on bad data.
- **Input**: CSV file with mixed valid and invalid dates in the target column.
- **Expected Behavior**:
    - Valid dates are converted.
    - Invalid dates are replaced with `ERROR`.
    - The script completes successfully without raising an exception.
- **Implementation Focus**: Try/Except blocks within the transformation loop.

## UC-6: Logging
**Goal**: Generate a detailed audit log of the operation.
- **Input**: CLI argument `-l conversion.log`.
- **Expected Behavior**:
    - A file `conversion.log` is created.
    - It contains lines formatted as: `File:input.csv Column:created original:05/Nov/25 5:16 PM converted:2025-11-05 17:16:00 --> successful`.
- **Implementation Focus**: Writing status strings to a file handler.
