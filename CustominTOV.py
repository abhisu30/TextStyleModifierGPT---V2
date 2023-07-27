import TokenCounter as TC
import openai
import os
from docx import Document

def createCustom(model, apikey, inputAuthorText, inputText, selectOutputFormat, customInstruction):
    messages =[]
    openai.api_key = apikey
    MODEL = model

    print("\n\INPUT TEXT" + str(inputText) + "\n\n")

    instruction = f"""
    
    TASK:
    - You are an AI Bot that is very good rephrasing the input text, denoted as INPUT TEXT, in the style denoted below NEW STYLE.
    - Your task is to rewrite the input text in the new style provided under the heading - NEW STYLE

    IMPORTANT INSTRUCTIONS:
    - Do not change the meaning of the input text, only rephrase it in the NEW STYLE.
    - Do not add any new information that is not provided in the input text.
    - Do not omit any information present in the input text.
    - Your output should consist of the INPUT TEXT written in the NEW STYLE.
       
    INPUT TEXT: 
    - {inputText}

    NEW STYLE:
    {customInstruction}
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
    token_count = TC.num_tokens_from_messages(messages, MODEL) + response_token
    
    doc = Document()
    doc.add_paragraph(output_raw)
    
    # Save the Word document.
    filename = "output_Custom.docx"
    doc.save(filename)
    
    return token_count, filename
