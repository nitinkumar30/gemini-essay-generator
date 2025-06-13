# Gemini Essay Generator
This project provides a Python script that leverages the Google Gemini API to generate essays or articles based on a predefined persona and prompt. It's designed to be robust with comprehensive error handling and easy to integrate into other Python applications.

## Features
1. Customizable Prompt: Easily modify the persona (e.g., student in 8th standard) and the essay topic.  
2. Word Count Control: The prompt dynamically includes a desired word count for the generated content.  
3. Error Handling: Includes try-except blocks to gracefully handle API errors such as network issues, rate limits, or safety-blocked content.  
4. Plain Text Output: Ensures the generated content is in plain text format, not Markdown.  
5. Modular Design: The core generation logic is encapsulated in a function, making it easy to import and reuse in other Python projects.  

## Prerequisites

Before you begin, ensure you have the following installed:

1. Python 3.7+

2. Google Generative AI Python Library (or just google ```pip install google~=3.0.0```):
```
pip install google-generativeai
```

## Configuration

### Gemini API Key
__You need a Google Gemini API Key to use this script.__

Generate your API Key: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your API key.

Directly in Code (Less Secure, for testing only):  
> While not recommended for production, you can directly replace "YOUR_API_KEY" in the [generateEssay.py](generateEssay.py) file with your actual API key:


## How to Run

1. Execute from Terminal
Navigate to the directory where you saved the file using your terminal or command prompt and run:

```
    python generateEssay.py
```
The script will:

1. Check for the API key.  
2. Configure the Gemini API.  
3. Generate the essay based on the defined prompts.
4. Print the prompt used and the generated output to your console.
5. Provide error messages if any issues occur during generation.

## How to Use (Importing into Other Files)
The generate_essay() function is designed to be easily imported and reused in other Python scripts.

1. Create Your Application File
Create a new Python file (e.g., main.py) in the same directory as generateEssay.py.

2. Import and Use the Function

Contents in [main.py](main.py)

3. Run generateEssay.py
```commandline
    python main.py
```

This will execute main.py, which in turn calls generate_essay() from [generateEssay.py](generateEssay.py), demonstrating seamless integration and reusability.

## Error Handling

1. The generate_essay function includes robust error handling for common API issues:
2. GEMINI_API_KEY Missing: The script will exit if the environment variable is not set.
3. API Configuration Errors: Catches issues during genai.configure().
4. genai.types.BlockedPromptException: Occurs if the prompt violates safety policies.
5. genai.types.StopCandidateException: Indicates that content generation was halted prematurely.
6. Generic Exception: Catches any other unexpected errors during the API call.

In case of an error, an informative message will be printed to sys.stderr, and the function will return None.

## Notes
Rate Limits: Be aware of the Gemini API rate limits to avoid unexpected service interruptions.
Model Selection: The script currently uses models/gemini-2.0-flash-lite-001. You can change this to [other available models](https://ai.google.dev/gemini-api/docs/rate-limits) as needed, but always check their specific rate limits and capabilities.

## Author

[Nitin Kumar](https://linkedin.com/in/nitin30kumar/)
