# promptType: argumentative, informational, narrative
# sub-dimension: (argument, persuasive), (expository, how-to, workplace), (descriptive, narrative)
# Purpose & Organization: (formatting, Main claim, Opener, Topic sentences, Concluding summary, impact message, Map, Cohesion), (formatting, thesis, opener, topic sentences, concluding summary, impact summary, map, cohesion), (formatting, topic focus, opener, event sequence, concluding reflection, cohesion)
# Development of ideas: (supporting claims, evidence, reasoning, transitions, counterclaim), (supporting points, evidence, transitions, reasoning), (events, descriptions, transitions)
# Language & Conventions: Sentence structure, vocabulary, spelling, grammar, capitalization, punctuation, Precise language

# promptType |=====|
# grade/instructionalLevel
# dimension

# ================ NOTES =================
# Pricing of the models ---> https://ai.google.dev/gemini-api/docs/rate-limits
# Generate API Key ---> https://aistudio.google.com/app/apikey

import google.generativeai as genai
import os
import sys
import pandas as pd  # Import the pandas library for CSV handling

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDq9Cws8HcaLyw8rJemCcDGSsRjDhcB3ys")

# --- Global Variables (can be overridden by CSV if you add these as columns) ---
TOTAL_WORDS_TO_BE_USED = 50
GRADE_LEVEL = 8
DEFAULT_EDITORIAL_PROMPT = (
    "Think of a problem that people face in your neighborhood or school. "
    "Write an editorial to your local newspaper presenting a solution to the problem you have identified."
)

# --- Model to use ---
MODEL_NAME = "models/gemini-2.0-flash-lite-001"

# --- Initialize Gemini Model ---
try:
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set the GEMINI_API_KEY environment variable to your Gemini API key.", file=sys.stderr)
        sys.exit(1)
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Error configuring Gemini API or initializing model: {e}", file=sys.stderr)
    sys.exit(1)


# --- Method to generate essay ---
def generate_essay_from_params(
        grade_level, total_words, prompt_type, sub_dimension, purpose_org, dev_of_ideas, lang_conventions,
        editorial_prompt_text
):

    starting_line = (
        f"You're a student in a well renowned school studying in {grade_level} standard. "
        f"Write down an essay on below topic with almost {total_words} words & use multiple paragraphs, if necessary. "
        f"Also, the tone of the article should be {prompt_type} & {sub_dimension} only. "
        f"Some sentences should be {purpose_org} & some should have a pinch of {dev_of_ideas}. "
        f"Also, put some errors in {lang_conventions}. Output should be in plain text only & not as markdown."
    )

    full_prompt = starting_line + '\n\n' + editorial_prompt_text

    try:
        response = gemini_model.generate_content(full_prompt)

        if response.parts:
            generated_text = ""
            for part in response.parts:
                if hasattr(part, 'text'):
                    generated_text += part.text
            if generated_text:
                return generated_text
            else:
                return "Warning: The API returned an empty text response."
        else:
            return "Warning: The API returned an empty response object or no parts."

    except genai.types.BlockedPromptException as e:
        feedback = e.response.prompt_feedback if hasattr(e.response, 'prompt_feedback') else 'No specific feedback.'
        return f"Error: Prompt blocked due to safety reasons. Details: {feedback}"
    except genai.types.StopCandidateException as e:
        finish_reason = e.candidate.finish_reason if hasattr(e.candidate, 'finish_reason') else 'Unknown reason.'
        return f"Error: Content generation stopped prematurely. Details: {finish_reason}"
    except Exception as e:
        return f"An unexpected error occurred during content generation: {e}"


def process_csv_and_generate_essays(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'. Please ensure the file exists.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file '{csv_file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    generated_responses = []

    print(f"Processing {len(df)} rows from '{csv_file_path}'...")

    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        print(f"--- Processing testID: {row['testID']} (Row {index + 1}/{len(df)}) ---")

        current_prompt_type = row.get('promptType', 'informational')  # Default if column not found
        current_sub_dimension = row.get('subDimension', 'expository')
        current_purpose_org = row.get('purposeOrg', 'thesis')
        current_dev_of_ideas = row.get('devOfIdeas', 'evidence')
        current_lang_conventions = row.get('langConventions', 'vocabulary')
        current_editorial_prompt = row.get('editorialPrompt',
                                           DEFAULT_EDITORIAL_PROMPT)
        current_grade_level = row.get('GRADE_LEVEL', GRADE_LEVEL)
        current_total_words = row.get('TOTAL_WORDS_TO_BE_USED', TOTAL_WORDS_TO_BE_USED)

        response_text = generate_essay_from_params(
            current_grade_level,
            current_total_words,
            current_prompt_type,
            current_sub_dimension,
            current_purpose_org,
            current_dev_of_ideas,
            current_lang_conventions,
            current_editorial_prompt
        )

        print(f"Generated Response (first 100 chars): {response_text[:100]}...\n")
        generated_responses.append(response_text)

    df['generatedResponse'] = generated_responses

    try:
        df.to_csv(csv_file_path, index=False)
        print(f"\nSuccessfully wrote generated responses to '{csv_file_path}' in 'generatedResponse' column.")
    except Exception as e:
        print(f"Error writing to CSV file '{csv_file_path}': {e}", file=sys.stderr)

process_csv_and_generate_essays('data.csv')

