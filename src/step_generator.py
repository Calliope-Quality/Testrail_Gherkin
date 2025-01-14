from pathlib import Path
from src import DEBUG
from src.openai_client import OpenAIClient

def generate_step_definitions(feature_file_path, step_file_path="steps/step_definitions.py", client=None):
    """
    Generate step definition skeletons for a given feature file and save them to a Python file.
    Optionally use OpenAI to enhance the step definitions.

    Args:
        feature_file_path (str): Path to the input Gherkin feature file.
        step_file_path (str): Path to save the generated step definitions.
        client (OpenAIClient): Optional OpenAI client for generating enhanced step definitions.

    Debugging is controlled via the global DEBUG flag in src/__init__.py.
    """
    try:
        # Debug input paths
        if DEBUG:
            print(f"[DEBUG] Reading feature file from: {feature_file_path}")
            print(f"[DEBUG] Writing step definitions to: {step_file_path}")

        # Ensure the feature file exists
        feature_file = Path(feature_file_path)
        if not feature_file.exists():
            print(f"[ERROR] Feature file not found: {feature_file_path}")
            return

        # Read the feature file
        with feature_file.open("r") as file:
            lines = file.readlines()

        if DEBUG:
            print(f"[DEBUG] Extracting steps from feature file.")

        # Extract unique Given, When, Then steps
        steps = []
        for line in lines:
            line = line.strip()
            if line.startswith(("Given", "When", "Then")):
                # Extract the step text and deduplicate
                clean_step = line.split(" ", 1)[1].strip()  # Remove the prefix (Given/When/Then)
                if clean_step not in steps:
                    steps.append(clean_step)

        if DEBUG:
            print(f"[DEBUG] Extracted steps: {steps}")

        # Generate step definition skeletons
        step_definitions = "from behave import given, when, then\n\n"
        for step in steps:
            if client:
                # Use OpenAI to generate enhanced step logic
                prompt = f"""
                Generate a Python implementation for the following Gherkin step:
                "{step}"

                Include comments and provide a sample implementation using Selenium or similar tools.
                """
                system_message = (
                    "You are an expert in Python test automation and behavior-driven development (BDD). "
                    "Provide step definition implementations for Gherkin steps using best practices in the Behave framework."
                )
                step_logic = client.generate_completion(prompt, system_message).strip()
            else:
                # Fallback: Provide a basic skeleton
                step_logic = f"""
    # TODO: Implement the logic for: "{step}"
    pass
"""

            step_definitions += f"""
@when("{step}")
def step_impl(context):
{step_logic}
"""

        # Ensure the output directory exists
        step_file = Path(step_file_path)
        step_file.parent.mkdir(parents=True, exist_ok=True)

        # Write the step definitions to the Python file
        with step_file.open("w") as file:
            file.write(step_definitions)

        print(f"[INFO] Step definitions saved: {step_file_path}")

    except Exception as e:
        print(f"[ERROR] Failed to generate step definitions: {e}")