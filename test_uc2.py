from jira_export_cleaner import convert_datetime

def test_convert_datetime():
    test_cases = [
        ("05/Nov/25 5:16 PM", "2025-11-05 17:16:00"),
        ("01/Jan/23 12:00 AM", "2023-01-01 00:00:00"),
        ("31/Dec/24 11:59 PM", "2024-12-31 23:59:00"),
        ("Invalid Date", "ERROR"),
        ("", "ERROR"),
        ("05/Nov/25 17:16", "ERROR"), # Wrong format
    ]

    print("Running tests for convert_datetime...")
    all_passed = True
    for input_str, expected in test_cases:
        result = convert_datetime(input_str)
        if result == expected:
            print(f"PASS: '{input_str}' -> '{result}'")
        else:
            print(f"FAIL: '{input_str}' -> '{result}' (Expected: '{expected}')")
            all_passed = False
    
    if all_passed:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    test_convert_datetime()
