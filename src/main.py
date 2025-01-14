import json
import os
from src import DEBUG
from src.feature_generator import generate_feature_file
from src.step_generator import generate_step_definitions
from src.openai_client import OpenAIClient
from src.test_case_importer import import_test_cases


def main():
    """
    Main function to process test cases and generate feature files and step definitions.
    Debugging is controlled via the global DEBUG flag in src/__init__.py.
    """
    # Dynamically resolve the path to config.json
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    config_path = os.path.join(script_dir, "../config/config.json")  # Move up to config folder

    # Load configuration
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file not found at: {config_path}")
        return

    # Enable debugging if specified
    if DEBUG:
        print(f"[DEBUG] Loaded configuration: {config}")

    # Get the test case file path from config
    file_path = config.get("TEST_CASE_FILE")
    if not file_path:
        print("[ERROR] TEST_CASE_FILE not found in config.json!")
        return

    # Import test cases
    test_cases = import_test_cases(file_path)

    # Initialize the OpenAI client
    client = OpenAIClient(config_path=config_path)

    # Process test cases
    for sheet_name, cases in test_cases.items():
        print(f"[INFO] Processing sheet: {sheet_name}")

        for case in cases:
            title = case.get("title")
            if not isinstance(title, str) or not title.strip():
                print(f"[ERROR] Invalid or missing title for test case in sheet '{sheet_name}'. Skipping this test case.")
                continue

            if DEBUG:
                print(f"[DEBUG] Processing test case: {title}")

            # Generate the feature file path
            feature_file_path = f"features/{title.replace(' ', '_').lower()}.feature"

            # Generate the feature file
            generate_feature_file(
                client=client,
                title=title,
                preconditions=case["preconditions"],
                steps=case["steps"],
                expected_results=case["expected_results"],
                output_folder="features"
            )

            # Generate the step definition file path
            step_file_path = f"steps/{title.replace(' ', '_').lower()}_steps.py"

            # Generate the step definitions with OpenAI client
            generate_step_definitions(
                feature_file_path=feature_file_path,
                step_file_path=step_file_path,
                client=client  # Pass the OpenAI client instance for step enhancement
            )

    print("[INFO] All feature files and step definitions have been successfully generated.")


if __name__ == "__main__":
    # Set DEBUG to True for detailed logs
    DEBUG = True  # Or False to disable debug logs
    main()