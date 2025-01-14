from pathlib import Path
from src import DEBUG
from src.openai_client import OpenAIClient


def generate_feature_file(client, title, preconditions, steps, expected_results, output_folder="features"):
    """
    Generate a Gherkin feature file for a test case and save it to the output folder.
    Debugging is controlled via the global DEBUG flag in src/__init__.py.

    Args:
        client (OpenAIClient): An instance of OpenAIClient for API interactions.
        title (str): Title of the test case.
        preconditions (str): Preconditions for the test case.
        steps (list): Steps of the test case.
        expected_results (list): Expected results for the test case.
        output_folder (str): Directory to save the generated feature file.
    """
    try:
        if DEBUG:
            print(f"[DEBUG] Generating feature file for: {title}")
            print(f"[DEBUG] Preconditions: {preconditions}")
            print(f"[DEBUG] Steps: {steps}")
            print(f"[DEBUG] Expected Results: {expected_results}")

        # Combine test case data into a single prompt
        prompt = f"""
        Convert the following test case into a well-structured Gherkin feature file:

        Title: {title}
        Preconditions: {preconditions}
        Steps:
        {chr(10).join([f"- {step}" for step in steps])}
        Expected Results:
        {chr(10).join([f"- {result}" for result in expected_results])}

        Ensure the feature file follows BDD principles and uses Given-When-Then syntax.
        """

        # System message for OpenAI to understand the context
        system_message = (
            "You are Calliope, an advanced AI and an expert in software testing, quality assurance, and electronic medical records "
            "(EMRs), especially in mental healthcare systems. Your goal is to evaluate test cases not only "
            "for QA best practices but also for their adherence to mental healthcare standards, compliance "
            "requirements, and clinical usability in an EMR system."
        )

        # Generate feature content using OpenAI
        feature_content = client.generate_completion(prompt, system_message)

        # Define the feature file path
        feature_file_name = f"{title.replace(' ', '_').lower()}.feature"
        feature_file_path = Path(output_folder) / feature_file_name

        # Ensure the output directory exists
        feature_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the feature file
        feature_file_path.write_text(feature_content)
        print(f"[INFO] Feature file saved: {feature_file_path}")

    except Exception as e:
        print(f"[ERROR] Failed to generate feature file for '{title}': {e}")