# Gherkinizer

This repository falls under the larger **Project Calliope** work.

---

## Overview

**Gherkinizer** is a Python-based automation tool designed to generate:
1. **Gherkin Feature Files** based on test cases from an Excel file.
2. **Step Definition Files** for use with the Behave framework, optionally enhanced by OpenAI’s API.

This project streamlines Behavior-Driven Development (BDD) workflows by automating the creation of feature files and step definitions, reducing manual effort.

---

## Features

- **Excel-Based Test Case Import:**
  - Reads test cases from an Excel file (multi-sheet support).
- **Gherkin Feature File Generation:**
  - Converts test cases into structured `.feature` files.
- **AI-Assisted Step Definition Generation:**
  - Uses OpenAI API to generate detailed step definition logic.
  - Provides comments and sample implementations.
- **Error Handling and Debugging:**
  - Logs errors and provides debug output for troubleshooting.

---

## Prerequisites

- **Python 3.8 or higher**
- Required libraries (install using `pip install -r requirements.txt`):
  - `openai`
  - `pandas`
  - `openpyxl`
- OpenAI API Key

---

## Project Structure

Testrail_Gherkin/
├── config/
│   └── config.json               # Configuration file (OpenAI API key and test case file path)
├── src/
│   ├── main.py                   # Main script
│   ├── feature_generator.py      # Gherkin feature file generator
│   ├── step_generator.py         # Step definition generator
│   ├── openai_client.py          # OpenAI client wrapper
│   ├── test_case_importer.py     # Excel test case importer
│   └── init.py               # Debug flag
├── tests/                        # Test case Excel files
├── .env                          # Environment variables (optional, for local use)
└── README.md                     # Project documentation

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/gherkinizer.git
   cd gherkinizer

	2.	Install Dependencies

pip install -r requirements.txt


	3.	Configure config.json
Create or edit config/config.json with your OpenAI API key and test case file path:

{
    "OPENAI_API_KEY": "your-openai-api-key",
    "TEST_CASE_FILE": "/absolute/path/to/your/test_case_file.xlsx"
}

Usage
	1.	Run the Main Script

python src/main.py


	2.	Output Files
	•	Feature Files:
	•	Saved in the features/ directory.
	•	File names are based on test case titles (e.g., add_patient.feature).
	•	Step Definitions:
	•	Saved in the steps/ directory.
	•	File names follow the format <test_case_title>_steps.py (e.g., add_patient_steps.py).

How It Works
	1.	Test Case Importer (test_case_importer.py)
	•	Reads test cases from an Excel file.
	•	Supports multi-sheet Excel files.
	•	Handles missing or grouped titles gracefully.
	2.	Feature File Generator (feature_generator.py)
	•	Converts test cases into .feature files using Gherkin syntax.
	•	Groups steps, preconditions, and expected results under scenarios.
	3.	Step Definition Generator (step_generator.py)
	•	Reads the generated feature file.
	•	Extracts Given, When, and Then steps.
	•	Uses OpenAI (if configured) to generate Python step logic.
	•	Saves step definitions in .py files.
	4.	OpenAI Integration (openai_client.py)
	•	Handles communication with OpenAI’s API.
	•	Generates enhanced step logic for step definitions.

Debugging
	•	Enable debug logs by setting DEBUG = True in src/__init__.py.
	•	Debug logs include:
	•	Loaded configuration.
	•	Extracted test case details.
	•	Generated file paths and content.

Examples

Input Excel File

Title	Pre-conditions	Steps	Expected Result
Add a new patient	User is logged in	Fill out all required fields	Patient added successfully
Verify appointment booking for patient	Patient exists in the system	Select date and time	Appointment booked successfully

Generated Feature File (features/add_patient.feature)

Feature: Add Patient
  Scenario: Add a new patient
    Given User is logged in
    When Fill out all required fields
    Then Patient added successfully

Generated Step Definitions (steps/add_patient_steps.py)

from behave import when

@when("Fill out all required fields")
def step_impl(context):
    """
    Use Selenium to locate and fill form fields.
    Example:
    - Locate "First Name" field and enter data.
    - Locate "Save" button and click it.
    """
    # TODO: Implement form-filling logic here
    context.driver.find_element(By.ID, "first_name").send_keys("John")
    context.driver.find_element(By.ID, "save_button").click()

Error Handling
	1.	Missing or Invalid Titles:
	•	Logs an error and skips the test case.
	2.	File Not Found:
	•	Logs an error if the Excel file or configuration file is missing.
	3.	OpenAI API Errors:
	•	Logs any API-related errors for debugging.

Customization
	•	Prompts for Step Definitions:
	•	Edit the prompt in step_generator.py to generate more detailed or specific step logic.
	•	Feature File Formatting:
	•	Modify feature_generator.py to adjust scenario formatting or add metadata.

Contributing

Contributions are welcome! To contribute:
	1.	Fork the repository.
	2.	Create a feature branch.
	3.	Submit a pull request.

License

This project is licensed under the MIT License.

Created by Adam Satterfield and Mike McDermott

