import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from PIL import Image

from app import df
from main import addlogo


addlogo()
st.set_page_config(page_title="Mooody - Dashboard", page_icon="photos/justcow_logo.png")
st.title("Moood Dashboard")
st.text("Welcome to your Moood Dashboard! Here, you can analyze your moods by filtering through your moods, reading your past journal entries, and more! 🚀🐮")
df['Date'] = pd.to_datetime(df['Date'])  



st.subheader("Filter moods")
available_cols = df.columns.tolist()
valid_moods = [m for m in ["Anger","Disgust","Fear","Joy","Neutral","Sadness","Surprise"] if m in available_cols]
selected_column = st.selectbox("Select mood to filter by", valid_moods)
st.write(df[["Date",selected_column, "Text"]])

st.markdown("""
<style>
span[data-baseweb="tag"]:has(span[title="Anger"]) {
  color: white;
  background-color: light-red;
}

span[data-baseweb="tag"]:has(span[title="Disgust"]) {
  color: white;
  background-color: #3CB371;
}

span[data-baseweb="tag"]:has(span[title="Fear"]) {
  color: white;
  background-color: #DDA0DD;
}
            
span[data-baseweb="tag"]:has(span[title="Joy"]) {
  color: white;
  background-color: orange;
}
            
span[data-baseweb="tag"]:has(span[title="Neutral"]) {
  color: white;
  background-color: grey;
}
            
span[data-baseweb="tag"]:has(span[title="Sadness"]) {
  color: white;
  background-color: #6495ED;
}
            
span[data-baseweb="tag"]:has(span[title="Surprise"]) {
  color: white;
  background-color: #48D1CC;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Mood Trends: Choose your mood!")
emotions_col = st.multiselect("Select mood(s) to plot", valid_moods)


if st.button("Generate Plot") and emotions_col:
    colors = []
    for em in emotions_col:
      if em == "Joy":
          colors.append("#edc02d")
      elif em == "Anger":
          colors.append("#ff5252")
      elif em == "Sadness":
          colors.append("#5269ff")
      elif em == "Fear":
          colors.append("#9d52ff")
      elif em == "Surprise":
          colors.append("#95eddd")
      elif em == "Disgust":
          colors.append("#aaed95")
      elif em == "Neutral":
          colors.append("#c3c4c2")
    st.line_chart(df.set_index('Date')[emotions_col],color=colors)


# happiness score chart
st.subheader("Happiness Score Over Time")
st.line_chart(df.set_index('Date')['Happiness Score'])