import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

#modified to sync with frontend

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model = "gemini-3.8-flash"

system_instruction = types.Part(text="""
Your name is Mr.Moo, you are a psychotherapist with a PhD in neuroscience. 
You have knowledge about CBT and other behavioural therapy techniques. 
You are patient with your clients, asking them questions to allow them to answer their own problems.
""")

def get_response(user_input, history=[]):
    contents = history + [types.Content(role="user", parts=[types.Part(text=user_input)])]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
        ],
        response_mime_type="text/plain",
        system_instruction=[system_instruction],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=config
    ):
        if chunk.text:
            response_text += chunk.text or ""

    # Update history
    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
    history.append(types.Content(role="model", parts=[types.Part(text=response_text)]))

    return response_text, history

