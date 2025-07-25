import os, sys, re, pandas as pd, google.generativeai as genai

# GEMINI_API_KEY = "AIzaSyAljFhakSkW718n3pSHJHW86Ef7Kweu2Mw"
# GEMINI_API_KEY = "AIzaSyDCYXVeNeyhSI5ZB-RVkWNmdjEpV4AbLyI"
GEMINI_API_KEY = "AIzaSyDbdt0f0eroyk3UCYPQBHZwVjPH5fim-mo"

MODEL_NAME = "models/gemini-2.0-flash-lite-001"

KEYWORDS = {
    "ses_mech_spelling": "spelling",
    "ses_mech_grammar": "grammar",
    "ses_mech_capitalization": "capitalization",
    "ses_mech_punctuation": "punctuation",
    "ses_mech_sent_struct": "sentence structure",
    "ses_mech_sentence_struc": "sentence structure",
    "ses_mech_vocabulary": "vocabulary",
    "ses_idea_qual_description": "descriptive",
    "ses_idea_qual_evidence": "evidence",
    "ses_idea_qual_relevant_claims": "relevant claims",
    "ses_idea_qual_narrative_events": "narrative events",
    "ses_org_formatting": "organization",
    "ses_org_intro_thesis": "organization",
    "ses_org_topic_sentences": "organization",
    "ses_org_event_sequence": "organization",
    "ses_org_establish_topic": "organization"
}
ERROR_PATTERN = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.I)

def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def trim_essay_to_word_count(text, target_word_count):
    words = text.split()
    if len(words) == target_word_count:
        return text
    elif len(words) > target_word_count:
        return " ".join(words[:target_word_count])
    else:
        return None  # too short, retry needed


def generate_essay(row, error_type, gemini_model, max_retries=3, allow_closest_match=True):
    grade = str(row.get('instructionalLevel', '6'))
    ptype = row.get('promptType', 'narrative')
    ptext = str(row.get('promptText', 'Write an essay on this topic.'))
    words = safe_int(row.get('no of words'), 100)
    errors_perc = row.get('% of errors', 0)
    errors_count = round(words * errors_perc if errors_perc <= 1 else words * errors_perc / 100)

    prompt = (
        f"You are a Grade {grade} student. Write a {ptype} essay on:\n\n\"{ptext}\"\n\n"
        f"Requirements:\n"
        f"- The essay must be exactly {words} words long (not more, not less).\n"
        f"- It must contain only {error_type} errors.\n"
        f"- It must contain only {errors_perc}% of {words} that is exactly {errors_count} number of only {error_type} errors.\n"
        f"- Use multiple paragraphs; separate them with '\\n' (new line).\n"
        f"- Do NOT start with any phrases like 'Here is my essay' or 'According to me'.\n"
        f"- Do NOT include introductions about the essay itself.\n"
        f"- Output ONLY the essay text, no markdown or extra formatting.\n"
        f"- Count words carefully to meet the exact length requirement and produce a strict output matching the word count.\n"
    )

    attempts = []
    for attempt in range(max_retries):
        try:
            response = gemini_model.generate_content(prompt)
            if not response.parts:
                print(f"Warning: Empty response from model on attempt {attempt + 1}")
                continue

            raw_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
            raw_text = re.sub(r"\s+", " ", raw_text).strip()
            word_list = raw_text.split()
            word_count = len(word_list)

            if word_count == words:
                return raw_text  # perfect match

            elif word_count > words:
                trimmed = " ".join(word_list[:words])
                attempts.append((trimmed, words))
            else:
                attempts.append((raw_text, word_count))

            print(f"Warning: Attempt {attempt + 1} generated {word_count} words, target is {words}")

        except Exception as e:
            print(f"Error generating essay on attempt {attempt + 1}: {e}")

    # After retries: return best effort or strict failure
    if allow_closest_match and attempts:
        closest = min(attempts, key=lambda x: abs(x[1] - words))
        print(f"⚠️ Returning closest match with {closest[1]} words (target {words})")
        return closest[0]

    print("❌ No valid essay generated." if not allow_closest_match else "⚠️ No essay generated, returning empty string")
    return "" if allow_closest_match else f"Failed to generate essay with correct length after {max_retries} attempts."


def generate_essays_to_column(csv_file_path, gemini_api_key):
    # Detect error type from filename
    match = ERROR_PATTERN.search(os.path.basename(csv_file_path).lower())
    error_type = KEYWORDS.get(match.group(), "spelling") if match else "spelling"
    print(f"✅ Detected error type: {error_type}")

    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}", file=sys.stderr)
        return

    # Check required columns
    required = ['instructionalLevel', 'promptType', 'promptText', 'no of words', 'total count errors', '% of errors']
    missing = [col for col in required if col not in df.columns]
    if missing:
        print(f"❌ Missing required columns: {', '.join(missing)}", file=sys.stderr)
        return

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        print(f"❌ Gemini Init Error: {e}", file=sys.stderr)
        return

    essays = []
    for i, row in df.iterrows():
        print(f"\n--- Row {i+1}/{len(df)} ---")
        essay_text = generate_essay(row, error_type, model)
        essays.append(essay_text)

    df['essay'] = essays
    df['AI generated content'] = 'YES'
    # Remove unwanted unnamed columns if any
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    try:
        df.to_csv(csv_file_path, index=False)
        print(f"\n✅ Saved essays to '{csv_file_path}' in 'essay' column.")
    except Exception as e:
        print(f"❌ Failed to save CSV: {e}", file=sys.stderr)

# Implementation ===>
generate_essays_to_column("ses_mech_spelling_informational_highlights.csv", GEMINI_API_KEY)
