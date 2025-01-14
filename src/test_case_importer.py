import pandas as pd


def import_test_cases(file_path):
    """
    Import test cases from an Excel file, handling grouped test case titles and missing data.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        dict: A dictionary where keys are sheet names and values are lists of test cases.
    """
    try:
        # Read all sheets from the Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)
        print(f"Successfully loaded test cases from: {file_path}")

        test_cases = {}

        for sheet_name, data in sheets.items():
            print(f"Processing sheet: {sheet_name}")

            if data.empty:
                print(f"[WARNING] Sheet '{sheet_name}' is empty. Skipping...")
                continue

            # Normalize column names to avoid case sensitivity
            data.columns = data.columns.str.strip().str.lower()

            # Ensure required columns exist
            required_columns = {"title", "pre-conditions", "steps", "expected result"}
            missing_columns = required_columns - set(data.columns)
            if missing_columns:
                print(f"[ERROR] Missing columns {missing_columns} in sheet '{sheet_name}'. Skipping this sheet.")
                continue

            # Initialize variables for processing grouped test cases
            current_title = None
            cases = []

            for _, row in data.iterrows():
                # Update the current title if it's present, else use the last valid one
                if pd.notna(row["title"]):
                    current_title = row["title"]

                if not current_title:
                    print("[ERROR] Encountered steps without a valid test case title. Skipping this row.")
                    continue

                # Extract data with default values for missing fields
                preconditions = row["pre-conditions"] if pd.notna(row["pre-conditions"]) else ""
                step = row["steps"] if pd.notna(row["steps"]) else ""
                expected_result = row["expected result"] if pd.notna(row["expected result"]) else ""

                # Group steps and expected results under the current test case title
                matching_case = next((case for case in cases if case["title"] == current_title), None)
                if not matching_case:
                    # Create a new test case entry if it doesn't exist
                    matching_case = {
                        "title": current_title,
                        "preconditions": preconditions,
                        "steps": [],
                        "expected_results": [],
                    }
                    cases.append(matching_case)

                # Append steps and expected results to the current test case
                if step:
                    matching_case["steps"].append(step)
                if expected_result:
                    matching_case["expected_results"].append(expected_result)

            # Add the processed cases to the output
            test_cases[sheet_name] = cases

        return test_cases

    except Exception as e:
        print(f"[ERROR] Failed to load test cases: {e}")
        raise