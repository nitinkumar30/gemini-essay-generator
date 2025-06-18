# ================ NOTES =================
# Pricing of the models ---> https://ai.google.dev/gemini-api/docs/rate-limits
# Generate API Key ---> https://aistudio.google.com/app/apikey

import google.generativeai as genai
# from google import genai
import os
import sys

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDq9Cws8HcaLyw8rJemCcDGSsRjDhcB3ys")

# --- Variables ---
TOTAL_WORDS_TO_BE_USED = 50
GRADE_LEVEL = 8
# promptType: argumentative, informational, narrative
# sub-dimension: (argument, persuasive), (expository, how-to, workplace), (descriptive, narrative)
# Purpose & Organization: (formatting, Main claim, Opener, Topic sentences, Concluding summary, impact message, Map, Cohesion), (formatting, thesis, opener, topic sentences, concluding summary, impact summary, map, cohesion), (formatting, topic focus, opener, event sequence, concluding reflection, cohesion)
# Development of ideas: (supporting claims, evidence, reasoning, transitions, counterclaim), (supporting points, evidence, transitions, reasoning), (events, descriptions, transitions)
# Language & Conventions: Sentence structure, vocabulary, spelling, grammar, capitalization, punctuation, Precise language
promptType = 'informational'
subDimension = 'expository'
purposeOrg = 'thesis'
devOfIdeas = 'evidence'
langConventions = 'vocabulary'


# STARTING_LINE = (
#     f"You're a student in a well renowned school studying in {GRADE_LEVEL} standard. Write down an essay on "
#     f"below topic with almost {TOTAL_WORDS_TO_BE_USED} words & use multiple para, if necessary. Output should be in plain "
#     f"text & not as markdown. Also, tone of the article should be ")
#
# EDITORIAL_PROMPT = (
#     "Think of a problem that people face in your neighborhood or school. "
#     "Write an editorial to your local newspaper presenting a solution to the problem you have identified."
# )

# --- Model to use ---
model = genai.GenerativeModel("models/gemini-2.0-flash-lite-001")


# --- Method to generate essay ---
def generate_essay(promptType, subDimension, purposeOrg, devOfIdeas, langConventions):

    STARTING_LINE = (
        f"You're a student in a well renowned school studying in {GRADE_LEVEL} standard. Write down an essay on "
        f"below topic with almost {TOTAL_WORDS_TO_BE_USED} words & use multiple para, if necessary. Also, tone of the "
        f"article should be {promptType} & {subDimension} only. Some sentences should be {purposeOrg} & some should "
        f"have a pinch of {devOfIdeas}. Also, put some errors in {langConventions}. Output should be in plain "
        f"text & not as markdown.")

    EDITORIAL_PROMPT = (
        "Think of a problem that people face in your neighborhood or school. "
        "Write an editorial to your local newspaper presenting a solution to the problem you have identified."
    )

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set the GEMINI_API_KEY environment variable to your Gemini API key.", file=sys.stderr)
        sys.exit(1)

    # Just to check API key is configured & ready to use
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error configuring Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

    # Actual code to run
    try:
        prompt = STARTING_LINE + '\n' + EDITORIAL_PROMPT
        response = model.generate_content(prompt)

        if hasattr(response, 'text') and response.text:
            print("Prompt used :->\n", prompt)
            print("\n\n\nGenerated output :->\n", response.text)
            # return response.text
        else:
            print("Warning: The API returned an empty response.", file=sys.stderr)

    except genai.types.BlockedPromptException as e:
        print(f"Error: The prompt was blocked due to safety reasons. Details: {e}", file=sys.stderr)
    except genai.types.StopCandidateException as e:
        print(f"Error: Content generation stopped prematurely. Details: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during content generation: {e}", file=sys.stderr)


generate_essay('informational', 'expository', 'thesis', 'evidence', 'vocabulary')
