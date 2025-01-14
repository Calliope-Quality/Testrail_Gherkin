import openai
import json
from src import DEBUG  # Import the global debug flag

class OpenAIClient:
    """
    OpenAIClient handles API interactions with OpenAI, including initializing the client
    and making requests for chat completions. Debug messages can be controlled globally.
    """
    def __init__(self, config_path):
        """
        Initialize the OpenAI client with the API key from the configuration file.

        Args:
            config_path (str): Path to the JSON config file containing the OpenAI API key.
        """
        self.debug = DEBUG  # Use the global debug flag for debug messages

        try:
            # Load the OpenAI API key from the config file
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            self.client = openai.OpenAI(api_key=config["OPENAI_API_KEY"])

            if self.debug:
                print(f"[DEBUG] OpenAI client initialized successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to initialize OpenAI client: {e}")
            raise

    def generate_completion(self, prompt, system_message):
        """
        Generate a chat completion from OpenAI using the provided prompt and system message.

        Args:
            prompt (str): The user-provided input prompt.
            system_message (str): The system message describing the assistant's behavior.

        Returns:
            str: The content of the generated chat completion.
        """
        try:
            if self.debug:
                print(f"[DEBUG] Sending prompt to OpenAI:\n{prompt}")
                print(f"[DEBUG] System message:\n{system_message}")

            # Create a chat completion using the correct API structure
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Calliope, an advanced AI who is an expert in software testing, Behavior Driven Development, Gherkin, quality assurance, and electronic medical records "
                            "(EMRs), especially in mental healthcare systems. Your goal is to evaluate test cases not "
                            "only for QA best practices but also for their adherence to mental healthcare standards, "
                            "compliance requirements, and clinical usability in an EMR system."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            # Extract the response content
            message_content = completion.choices[0].message.content

            if self.debug:
                print(f"[DEBUG] OpenAI response received:\n{message_content}")

            return message_content
        except openai.error.OpenAIError as e:
            print(f"[ERROR] OpenAI API error: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Unexpected error during OpenAI API call: {e}")
            raise