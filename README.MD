# Gemini Essay Generator

1. This Python script automates the generation of essays using the Google Gemini API. 
2. It reads input parameters from a CSV file, crafts dynamic prompts based on these parameters, sends them to the Gemini model, and then writes the generated responses back into the same CSV file.


## Features
1. CSV-Driven Input: Reads various essay parameters (grade level, word count, prompt type, editorial prompt, etc.) directly from a CSV file.
2. Dynamic Prompt Generation: Constructs specific and detailed prompts for the Gemini API based on the data in each CSV row, allowing for highly customized content creation.
3. Google Gemini API Integration: Utilizes the google-generativeai library to interact with the Gemini large language models, ensuring access to cutting-edge AI capabilities.
4. CSV Output: Appends a new column named 'generatedResponse' to your input CSV file, containing the AI-generated essays. If the column already exists, it will be updated with new content.
5. Robust Error Handling: Includes comprehensive error handling for API key configuration, file operations, and common Gemini API response issues (e.g., blocked prompts, premature stops), making the script reliable for automated tasks.


## Advantages Over Manual Effort

This project offers significant advantages by automating content generation, which would otherwise be a tedious and time-consuming manual process:
1. Efficiency at Scale: Generate dozens, hundreds, or even thousands of unique essays or articles in minutes by simply populating a CSV file. This is impossible to achieve manually in a comparable timeframe.
2. Consistency and Customization: Maintain a consistent persona, tone, and specific requirements (like word count, thesis statements, or vocabulary errors) across all generated content, ensuring a uniform output that can be precisely controlled via CSV inputs. This includes the ability to dynamically control the persona and essay topic, as well as the desired word count.
3. Reduced Human Error: Automating the generation process minimizes the potential for human errors in writing, formatting, or adhering to specific prompt instructions.
4. Plain Text Output: Ensures that the generated content is in plain text format, which is easy to integrate into various systems and applications without additional formatting conversion.
5. Cost-Effective Prototyping: Quickly generate varied content for testing, prototyping, or large-scale data synthesis without the need for extensive manual writing resources.

## Working

[![Working of this project](essayWritingUsingPrompts.gif)](essayWritingUsingPrompts.gif)


## Versatility and Applications
The modular design and flexible input mechanism of this essay generator make it highly versatile and applicable to various scenarios:
1. Educational Content Creation:
   - Generate practice essays for students across different grade levels and writing styles.
   - Create diverse examples of argumentative, informational, or narrative writing.
   - Produce content for language learning, specifically focusing on introducing vocabulary errors or demonstrating grammatical structures.
2. Content Marketing & Blogging:
   - Rapidly draft article outlines or short blog posts on various topics by simply changing the editorial Prompt and other parameters.
   - Generate variations of marketing copy for A/B testing.
3. Automated Report Generation:
   - Produce summary reports or editorial pieces based on structured data inputs, automating parts of documentation creation.
4. AI Model Testing and Evaluation:
   - Generate large datasets of diverse prompts and expected outputs for testing and fine-tuning other language models.
   - Evaluate how well different Gemini models or configurations perform under specific constraints (e.g., word count, tone, inclusion of "errors").
5. Creative Writing Exploration:
   - Experiment with different writing styles, personas, and narrative structures by simply modifying CSV inputs.
6. Modular Design for Reusability: The core generation logic is encapsulated in functions, making it easy to import and reuse in other Python projects or larger applications.

This project empowers users to leverage the power of generative AI efficiently, significantly reducing manual effort and opening up new possibilities for content creation and data synthesis.


## Model Information and Usage Limits

This script utilizes the [gemini-1.5-flash-001](https://ai.google.dev/gemini-api/docs/models#gemini-1.5-flash) model, a highly efficient and capable model from the Gemini family.
1. Free Tier Usage: The Gemini API offers a free tier that allows you to experiment and build applications within certain usage limits. These limits are subject to change, and it's essential to consult the official documentation for the most up-to-date information on quotas and pricing.
2. Checking Rate Limits: You can find detailed information on model pricing and rate limits at Google AI for Developers - Rate Limits. Be aware of these limits to avoid unexpected service interruptions or billing.


## Prerequisites

Before running the script, ensure you have the following installed:
- pandas
- google-generativeai


## Setup

1. Install Dependencies:  

    Open your terminal or command prompt and run:
    ```commandline
    pip install -r requirements.txt
    ```

2. Configure Gemini API Key:  

The script requires your Google Gemini API key. For security reasons, never hardcode your API key in the script. Instead, set it as an environment variable named 'GEMINI_API_KEY'.

- Get your API Key: If you don't have one, generate it from Google AI Studio.
    - Set Environment Variable:
        - Linux/macOS:
        ```export GEMINI_API_KEY="YOUR_API_KEY_HERE"```
        (Add this line to your ~/.bashrc, ~/.zshrc, or ~/.profile for persistence)
        - Windows (Command Prompt):
          ```set GEMINI_API_KEY="YOUR_API_KEY_HERE"```
        - Windows (PowerShell):
          ```$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"```
        (For persistence, set it in System Environment Variables via Control Panel/System Settings)


## CSV File Format

The script expects an input CSV file with specific column headers. Make sure your CSV file (e.g., input_prompts.csv) includes at least the following columns:
- testID: A unique identifier for each test case (e.g., 1, 2, 3).
- promptType: The general tone/type of the essay (e.g., informational, argumentative, narrative).
- subDimension: A more specific sub-type (e.g., expository, persuasive, descriptive).
- purposeOrg: Focus on purpose/organization (e.g., thesis, Main claim, topic focus).
- devOfIdeas: Focus on development of ideas (e.g., evidence, supporting claims, events).
- langConventions: Focus on language conventions (e.g., vocabulary, spelling, grammar).
- GRADE_LEVEL: The student's grade level (e.g., 8, 9, 7).
- TOTAL_WORDS_TO_BE_USED: Approximate word count for the essay (e.g., 50, 70, 60).
- editorialPrompt: The specific problem/topic for the editorial (e.g., "Think of a problem... solution...").

**Example [data.csv](data.csv) content:**

```
testID,promptType,subDimension,purposeOrg,devOfIdeas,langConventions,GRADE_LEVEL,TOTAL_WORDS_TO_BE_USED,editorialPrompt
1,informational,expository,thesis,evidence,vocabulary,8,50,"Think of a problem that people face in your neighborhood or school. Write an editorial to your local newspaper presenting a solution to the problem you have identified."
2,argumentative,persuasive,Main claim,supporting claims,spelling,9,70,"Imagine you are advocating for a new recycling program in your community. Write a persuasive editorial for the local newspaper."
3,narrative,descriptive,topic focus,events,grammar,7,60,"Describe a typical day at your school, focusing on a specific event or activity that makes it unique."
```
        
              
## How to Run

1. Save your CSV: Ensure your input CSV file (e.g., data.csv) is in the same directory as your Python script, or provide the full path to it within the script.
2. Execute the script:

    ```python main.py```

> The script will process each row, print progress to the console, and then update the [data.csv](data.csv) file with a new generatedResponse column.


## Output
The generatedResponse column in your [data.csv](data.csv) file will contain the AI-generated essay text for each corresponding row's parameters.


## Troubleshooting

1. ModuleNotFoundError: Make sure you've installed all dependencies using pip.
2. API Key Errors: Verify your GEMINI_API_KEY environment variable is correctly set and your API key is valid.
3. BlockedPromptException / StopCandidateException: Review your prompt content for safety guideline violations or consider adjusting API safety settings (refer to Google Gemini API documentation for details).


## Author

[Nitin Kumar](https://linkedin.com/in/nitin30kumar/)
