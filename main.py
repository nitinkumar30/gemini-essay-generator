# my_app.py

import sys
# Import the generate_essay function from optimized_gemini_script
from generateEssay import generate_essay


def main():
    """
    Main function to demonstrate importing and using the essay generation.
    """
    print("Attempting to generate an essay using the imported function...")

    # Call the generate_essay function to get the generated content
    generated_content = generate_essay()

    if generated_content:
        print("\nSuccessfully received generated content in my_app.py:")
        print("--- Start of Imported Content ---")
        print(generated_content)
        print("--- End of Imported Content ---")

        # You can now further process or use 'generated_content' here.
        # For example, save it to a new file:
        try:
            with open("generated_editorial.txt", "w", encoding="utf-8") as f:
                f.write(generated_content)
            print("\nContent successfully saved to generated_editorial.txt")
        except IOError as e:
            print(f"Error: Could not save content to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nFailed to generate content or received an empty response in my_app.py.")
        print("Please review the output from 'optimized_gemini_script' for any error messages.")
        sys.exit(1)  # Exit with an error code to indicate failure


if __name__ == "__main__":
    # Execute the main function when the script is run directly
    main()

