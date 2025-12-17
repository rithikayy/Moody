import streamlit as st
from main import analyzelog
import pandas as pd
from google import genai
from google.genai import types
from main import addlogo
import os
from dotenv import load_dotenv

file_path = "data.csv"

load_dotenv()
addlogo()

columns = ["Date", "Anger","Disgust","Fear","Joy","Neutral","Sadness","Surprise","Happiness Score", "Text"]

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=columns)

# df = pd.DataFrame(columns=columns) 

def add_to_df(data, df):
    df.loc[len(df)] = data
    df.to_csv(file_path, index=False)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please add your Gemini API key to a .env file.")

client = genai.Client(api_key=api_key)

def ask_ai(df):
   data_frame = df.sort_values(by='Date') 
   if not data_frame.empty:
       latest_entry = data_frame.iloc[-1]['Text']
   else:
       latest_entry = "No journal entries yet."
    
   return "How's your day"

#    new_q = latest_entry + "Ask a question based on this journal entry. Keep it open-ended and be specific! If it's empty or not much content, just ask a basic open-ended question like 'how's your day?' BE STRAIGHTFORWARD AND BRIEF. DO NOT MAKE UP YOUR OWN JOURNAL ENTRY"

#    response = client.models.generate_content(
#        model="gemini-2.5-flash",
#        contents=new_q,
#        config=types.GenerateContentConfig(
#            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
#        ),
#    )
#    return response.text

home_page = st.Page(
    "views/homepage.py",
    title="Welcome to Mooody!"
)
project_1_page = st.Page(
    "views/journal.py",
    title="Journal"
)
project_2_page = st.Page(
    "views/frontendtherapist.py",
    title="Therapist Bot",
)
project_3_page = st.Page(
    "views/mood_dashboard.py",
    title = "Mood Dashboard"
)
project_4_page = st.Page(
    "views/draw.py",
    title = "Sketchbook"
)

with open("src/styles.css", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

pg = st.navigation([home_page, project_1_page, project_2_page, project_3_page, project_4_page])

pg.run()

# if text_input:
#    data_row = analyzelog(text_input)
#    new_row = pd.DataFrame([data_row], columns=df.columns)
#    df = pd.concat([df, new_row], ignore_index=True)
#    df['Date'] = pd.to_datetime(df['Date'])
#    st.subheader("Happiness Score Over Time")
#    st.line_chart(df.set_index('Date')['Happiness_Score'])
