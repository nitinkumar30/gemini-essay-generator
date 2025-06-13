# ================ NOTES =================
# Pricing of the models ---> https://ai.google.dev/gemini-api/docs/rate-limits
# Generate API Key ---> https://aistudio.google.com/app/apikey

import google.generativeai as genai
import os
import sys

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# --- Variables ---
TOTAL_WORDS_TO_BE_USED = 500

STARTING_LINE = (
    "You're a student in a well renowned school studying in 8th standard. Write down an article/essay on "
    f"below topic with almost {TOTAL_WORDS_TO_BE_USED} words paragraph wise, if necessary. Output should be in plain "
    f"text & not as markdown:")

EDITORIAL_PROMPT = (
    "Think of a problem that people face in your neighborhood or school. "
    "Write an editorial to your local newspaper presenting a solution to the problem you have identified."
)

# --- Model to use ---
model = genai.GenerativeModel("models/gemini-2.0-flash-lite-001")


# --- Method to generate essay ---
def generate_essay():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set the GEMINI_API_KEY environment variable to your Gemini API key.", file=sys.stderr)
        sys.exit(1)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error configuring Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        response = model.generate_content(STARTING_LINE + EDITORIAL_PROMPT)

        if hasattr(response, 'text') and response.text:
            print("Prompt used :->\n", STARTING_LINE + EDITORIAL_PROMPT)
            print("\n\n\nGenerated output :->\n", response.text)
            return response.text
        else:
            print("Warning: The API returned an empty response.", file=sys.stderr)

    except genai.types.BlockedPromptException as e:
        print(f"Error: The prompt was blocked due to safety reasons. Details: {e}", file=sys.stderr)
    except genai.types.StopCandidateException as e:
        print(f"Error: Content generation stopped prematurely. Details: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during content generation: {e}", file=sys.stderr)


