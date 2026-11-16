import streamlit as st
from google.genai import types
from google import genai
from app import client, add_to_df, df
from datetime import date
import re

def sketchai(pic_path):
  with open(pic_path, 'rb') as f:
      image_bytes = f.read()

  prompt = (
      "Return the probabilities (in decimal that adds up to 1.0) for each category in this format:\n\n"
      "{\n"
      "  'Anger': %, \n"
      "  'Disgust': %, \n"
      "  'Fear': %, \n"
      "  'Joy': %, \n"
      "  'Neutral': %, \n"
      "  'Sadness': %, \n"
      "  'Surprise': %\n"
      "}\n"

      "AND DONT ADD ANY INTRO OR ANYTHING ELSE!!!!!"
  )

  response = client.models.generate_content(
      model='gemini-3.8-flash',
      contents=[
        types.Part.from_bytes(
          data=image_bytes,
          mime_type='image/jpeg',
        ),
        prompt
      ]
    )

  # sample output:
  # {
  #   'anger': 0.05,
  #   'disgust': 0.05,
  #   'fear': 0.30,
  #   'joy': 0.25,
  #   'neutral': 0.00,
  #   'sadness': 0.30,
  #   'surprise': 0.05
  # }

  new_q = ("describe the drawing in one or two sentences max.")

  draw_response = client.models.generate_content(
      model='gemini-3.8-flash',
      contents=[
        types.Part.from_bytes(
          data=image_bytes,
          mime_type='image/jpeg',
        ),
        new_q
      ]
    )

  moods_split = response.text.split(",")
  mood_vals = []
  for mood in moods_split:
    mood_vals.extend(re.findall(r' \d.\d', mood))

  for i in range(0, len(mood_vals)):
    mood_vals[i] = float(mood_vals[i])

  anger = mood_vals[0]
  disgust = mood_vals[1]
  fear = mood_vals[2]
  joy = mood_vals[3]
  neutral = mood_vals[4]
  sadness = mood_vals[5]
  surprise = mood_vals[6]

  happiness_score = mood_vals[0]*1 + mood_vals[1]*4 + mood_vals[2]*2 + mood_vals[3]*10 + mood_vals[4]*5 +mood_vals[5]*1 + mood_vals[6]*6
  data = [date.today(), anger, disgust, fear, joy, neutral, sadness, surprise, round(happiness_score), draw_response.text]
  add_to_df(data, df)

