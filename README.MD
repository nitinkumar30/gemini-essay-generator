# AI Essay Generator with Gemini 📝

> 1. This Python script leverages the Google Gemini API to automate the generation of essays based on specific criteria defined in a CSV file. It's engineered to create datasets of student-like essays, complete with a specified type and percentage of errors, making it ideal for training NLP models, developing educational software, or generating content at scale.
> 2. The script intelligently infers the desired error type (e.g., `spelling`, `grammar`, `punctuation`) from the input CSV's filename, generates a unique essay for each row, and saves the output directly back into the same file, creating a seamless and efficient workflow.

---

## ✨ Features 

* **🤖 Gemini-Powered Generation**: Utilizes the powerful `gemini-2.0-flash-lite-001` model, which is optimized for high-quality, context-aware text generation at speed, making it perfect for batch-processing tasks.
* **🎯 Dynamic Error Injection**: Goes beyond simple generation by using sophisticated prompt engineering to instruct the AI to introduce a precise *type* and *quantity* of errors. This allows for the creation of nuanced datasets that mimic real-world student writing challenges.
* **📂 Filename-Driven Configuration**: Automatically detects the desired error category (e.g., `spelling`, `grammar`, `organization`) by matching keywords in the input CSV's filename. This feature makes the tool incredibly flexible, allowing you to switch generation contexts simply by renaming a file, with no code changes required.
* **📊 CSV-Driven Workflow**: Reads all essay parameters—grade level, prompt, word count, and error percentage—directly from a structured CSV file. This enables the batch processing of hundreds of diverse essay requirements in a single run.
* **📏 Strict Word Count Control**: Implements a robust retry mechanism and a smart post-processing logic to ensure the generated essays meet an **exact** word count. If a perfect match isn't found after several attempts, it intelligently identifies and returns the attempt that is closest to the target length, ensuring you always get a usable result.
* **✅ In-place CSV Updating**: Appends the generated essays and an 'AI generated' tag into new columns (`essay`, `AI generated content`) in the original CSV file. This streamlines the data creation pipeline by keeping your inputs and outputs consolidated in one place.
* **🛡️ Robust Error Handling**: Includes preemptive checks for missing CSV files, required columns, and API initialization errors to ensure smooth execution and provide clear, actionable feedback if something goes wrong.

---

## Working

[![Working of this project](essayWritingsUsingPrompts.gif)](essayWritingsUsingPrompts.gif)

## 🚀 Advantages & Applications

This tool offers significant advantages by automating what would otherwise be a tedious, error-prone, and time-consuming manual process.

### Why Automate?

* **Efficiency at Scale**: Manually writing a dozen essays to specific constraints could take hours. This script can generate hundreds or even thousands of unique, rule-compliant essays in minutes. You simply populate a CSV file, and the generator handles the rest.
* **Consistency & Customization**: Achieve a level of consistency that is impossible with manual writing. Maintain a specific persona, tone, and set of requirements (like word count or error types) across all generated content, ensuring a uniform dataset that can be precisely controlled via CSV inputs.
* **Reduced Human Error**: Automating the generation process minimizes the potential for human mistakes in writing, formatting, or adhering to complex prompt instructions, leading to cleaner, more reliable datasets.

### Versatility

The modular design makes this generator highly applicable to a wide range of scenarios:

1.  **Educational Content & AI Training**:
    * Generate large, diverse datasets of student writing with controlled errors to train and validate grammar/spelling correction models. For example, create 1,000 essays with precisely 5% capitalization errors.
    * Create examples of argumentative, informational, or narrative essays for different grade levels to be used as teaching aids or in assessment platforms.

2.  **Content Marketing & SEO**:
    * Rapidly draft multiple variations of article outlines or short blog posts on various topics by simply changing the `promptText` and other parameters in the CSV.

3.  **AI Model Testing and Evaluation**:
    * Generate large datasets to benchmark and fine-tune other language models.
    * Evaluate how well different AI models perform under strict constraints (e.g., word count, tone, error injection), providing valuable data on model compliance and reliability.

---

## ⚙️ How It Works

The script follows a simple, fully automated, multi-step process for each row in your input file:

1.  **Detect Error Type**: Before processing begins, the script inspects the name of the input CSV file (e.g., `data_ses_mech_spelling.csv`). It matches keywords from the filename against its internal `KEYWORDS` dictionary to determine which error type to focus on (`spelling`, `grammar`, etc.) for the entire batch.
2.  **Read Input CSV**: It loads the specified CSV file into a pandas DataFrame and performs a crucial validation step to ensure all required columns are present, preventing runtime errors.
3.  **Iterate and Prompt**: For each row in the DataFrame, it dynamically constructs a detailed, multi-part prompt for the Gemini model. This prompt meticulously weaves together the grade level, essay topic, essay type, and strict instructions on the exact word count and the number/type of errors to include.
4.  **Generate and Validate**: It sends the complete prompt to the Gemini API. The script then enters a validation loop, attempting up to three times (`max_retries=3`) to get a response that perfectly matches the word count. If a generated essay is too long, it's precisely trimmed; if it's too short or the generation fails, the script automatically retries. This validation is critical for producing clean, predictable datasets.
5.  **Update and Save**: Once a valid essay is secured, it's added to a new `essay` column in the DataFrame. A second column, `AI generated content`, is also added and set to `YES`. Finally, the updated DataFrame is saved, overwriting the original CSV file with the new, enriched data.

---

## 📋 Getting Started

### Prerequisites

* Python 3.7+
* A Google Gemini API Key. You can get a free key from **[Google AI Studio](https://aistudio.google.com/app/apikey)**.

### Installation

1.  **Clone the repository or save the script:**
    ```bash
    git clone https://github.com/nitinkumar30/gemini-essay-generator
    cd gemini-essay-generator
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install pandas google-generativeai
    ```

3.  **Set up your API Key:**
    For security and best practices, it is highly recommended to set your API key as an environment variable rather than hardcoding it.

    * **Linux/macOS:**
        ```bash
        export GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    * **Windows (PowerShell):**
        ```powershell
        $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    The script is designed to automatically find and use this environment variable.

---

## USAGE

### 1. Prepare Your Input CSV

Your CSV file **must** contain the following columns. The column names must match exactly.

| Column Name          | Type      | Description                                                                                             | Example                                |
| -------------------- | --------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `instructionalLevel` | Integer   | The grade level of the student persona the AI should adopt. This influences vocabulary and sentence complexity. | `8`                                    |
| `promptType`         | String    | The high-level style of the essay (e.g., `narrative`, `informational`, `argumentative`).                  | `narrative`                            |
| `promptText`         | String    | The specific topic, question, or instruction for the essay.                                             | `Write a story about a hidden treasure.` |
| `no of words`        | Integer   | The **exact** target word count for the final essay. The script will work to meet this number precisely.  | `150`                                  |
| `% of errors`        | Float/Int | The percentage of words that should contain the specified error. `10` and `0.1` are both valid.           | `10` or `0.1`                          |
| `total count errors` | Integer   | (Optional, for reference) The total number of errors. The script calculates this from `% of errors`.      | `15`                                   |

### 2. Name Your CSV File Correctly

The script determines the error type for the entire batch from the filename. Ensure your filename contains one of the keywords defined in the `KEYWORDS` dictionary.

**Examples:**

* `data_grade5_ses_mech_spelling.csv` ➡️ will generate essays with **spelling** errors.
* `informational_ses_org_intro_thesis.csv` ➡️ will generate essays with **organization** errors related to the thesis.
* `narrative_prompts.csv` ➡️ will default to **spelling** errors if no keyword is matched.

### 3. Run the Script

Modify the last line of the script to point to your CSV file.

```python
# Implementation ===>
import os

# The script will automatically fetch the API key from your environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Call the main function with the path to your CSV file
if GEMINI_API_KEY:
    generate_essays_to_column("ses_mech_spelling_informational_highlights.csv", GEMINI_API_KEY)
else:
    print("❌ Error: GEMINI_API_KEY environment variable not set.")
```

Execute the script from your terminal:

```commandline
python main.py
```

> The script will print its progress to the console, row by row, and save the final results directly in your CSV file upon completion.

## Troubleshooting

1. API Key Errors: Ensure your GEMINI_API_KEY environment variable is correctly set, has no extra spaces or characters, and that the key itself is valid and enabled in your Google AI Studio project.
2. FileNotFoundError: Double-check that the path to your CSV file in the generate_essays_to_column() function call is correct and that the script is being run from the correct directory.
3. Missing Columns Error: Carefully verify that your CSV file contains all the required headers as listed in the "Prepare Your Input CSV" section. Column names are case-sensitive.
4. Empty Responses: If the model returns empty responses, it might be due to overly restrictive safety filters on the API or an ambiguous promptText. Try adjusting the prompt to be more open-ended, or check the safety settings in your Google AI project. This can also happen due to intermittent network issues.

### Author

[Nitin Kumar](https://linkedin.com/in/nitin30kumar/)
