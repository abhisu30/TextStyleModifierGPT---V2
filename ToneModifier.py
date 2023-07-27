import TokenCounter as TC
import openai
import os
from docx import Document


def toneDescriberGPT(apikey, model, inputAuthorText):
    messages =[]
    openai.api_key = apikey
    MODEL = model

    instruction = f"""
    % YOUR TASK:
    - You are an expert AI that is capable of analyzing the writing tone of the input text and decribing the tone based on the factors provided below.
    - Describe the tone of the input text using all the following factors described below.

    % HOW TO DESCRIBE TONE:
    1. Pace: The speed at which the story unfolds and events occur.
    2. Mood: The overall emotional atmosphere or feeling of the piece.
    3. Tone: The author's attitude towards the subject matter or characters.
    4. Voice: The unique style and personality of the author as it comes through in the writing.
    5. Diction: The choice of words and phrases used by the author.
    6. Syntax: The arrangement of words and phrases to create well-formed sentences.
    7. Imagery: The use of vivid and descriptive language to create mental images for the reader.
    8. Theme: The central idea or message of the piece.
    9. Point of View: The perspective from which the story is told (first person, third person, etc.).
    10. Structure: The organization and arrangement of the piece, including its chapters, sections, or stanzas.
    11. Dialogue: The conversations between characters in the piece.
    12. Characterization: The way the author presents and develops characters in the story.
    13. Setting: The time and place in which the story takes place.
    14. Foreshadowing: The use of hints or clues to suggest future events in the story.
    15. Irony: The use of words or situations to convey a meaning that is opposite of its literal meaning.
    16. Symbolism: The use of objects, characters, or events to represent abstract ideas or concepts.
    17. Allusion: A reference to another work of literature, person, or event within the piece.
    18. Conflict: The struggle between opposing forces or characters in the story.
    19. Suspense: The tension or excitement created by uncertainty about what will happen next in the story.
    20. Climax: The turning point or most intense moment in the story.
    21. Resolution: The conclusion of the story, where conflicts are resolved and loose ends are tied up.

    % START of Author Writing: 
    {inputAuthorText}
    % END OF Author Writing

    """
    input = str(instruction)
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input},
    ],
    temperature=0,
    )

    tone = response['choices'][0]['message']['content']

    print("\n\nTONE" + str(tone) + "\n\n")

    response_token = response["usage"]["prompt_tokens"]
    token_count1 = TC.num_tokens_from_messages(messages, MODEL) + response_token

    return token_count1, tone

def authorFinderGPT(apikey, model, inputAuthorText):

    messages =[]
    openai.api_key = apikey
    MODEL = model

    instruction = f"""
    - You are an expert AI that is very good at identifying authors, public figures, or writers whose style matches a piece of input text.
    - Your goal is to identify which authors, public figures, or writers sound most similar to the text below.

    % START Author Writing
    {inputAuthorText}
    % END Author Writing

    - List up to 4 authors whose writing styles most closely resemble the examples above. 
    - Only respond with the names separated by commas.
    """
    input = str(instruction)
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input},
    ],
    temperature=0,
    )

    authors = response['choices'][0]['message']['content']

    print("\n\nTONE" + str(authors) + "\n\n")

    response_token = response["usage"]["prompt_tokens"]
    token_count2 = TC.num_tokens_from_messages(messages, MODEL) + response_token

    return token_count2, authors

def Tonechanger(model, apikey, inputAuthorText, inputText, selectOutputFormat, customInstruction):
    messages =[]
    openai.api_key = apikey
    MODEL = model

    token_count1, tone = toneDescriberGPT(apikey, model, inputAuthorText)
    token_count2, authors = authorFinderGPT(apikey, model, inputAuthorText)

    print("\n\INPUT TEXT" + str(inputText) + "\n\n")

    instruction = f"""
    
    TASK:
    - You are an AI Bot that is very good rephrasing the input text, denoted as INPUT TEXT, to sound like the author writing style, denoted as AUTHOR WRITING.
    - Use the Autor tone, denoted as AUTHOR TONE to change the tone of the input text.

    IMPORTANT INSTRUCTIONS:
    - Do not change the meaning of the input text, only mimic the author style of writing.
    - Do not use any aspect of the AUTHOR WRITING in your output.
    - Do not add any new information that is not provided in the input text.
    - Do not omit any information present in the input text.
    - Your output should consist of the INPUT TEXT written in the style of the author writing style.
       
    INPUT TEXT: 
    - {inputText}

    LIST OF AUTHORS:
    {authors}
    
    AUTHOR TONE:
    - {tone}

    AUTHOR WRITING: 
    - {inputAuthorText}
    """
    input = str(instruction)
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input},
    ],
    temperature=0,
    )

    output_raw = response['choices'][0]['message']['content']
    response_token = response["usage"]["prompt_tokens"]
    token_count3 = TC.num_tokens_from_messages(messages, MODEL) + response_token
    
    doc = Document()
    doc.add_paragraph(output_raw)
    
    # Save the Word document.
    filename = "output.docx"
    doc.save(filename)

    token_count = token_count1 + token_count2 + token_count3
    
    return token_count, filename
