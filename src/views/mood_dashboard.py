import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

from app import df
from main import addlogo


addlogo()
st.set_page_config(page_title="Mooody - Dashboard", page_icon="photos/justcow_logo.png")
st.title("Moood Dashboard")
st.text("Welcome to your Moood Dashboard! Here, you can analyze your moods by filtering through your moods, reading your past journal entries, and more! 🚀🐮")
df['Date'] = pd.to_datetime(df['Date'])  



st.subheader("Filter moods")
available_cols = df.columns.tolist()
valid_moods = [m for m in ["Anger","Disgust","Fear","Joy","Neutral","Sadness","Surprise","Happiness Score"] if m in available_cols]
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
            
span[data-baseweb="tag"]:has(span[title="Happiness Score"]) {
  color: white;
  background-color: #5adb8e;
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
      else:
          colors.append("#5adb8e")
    st.line_chart(df.set_index('Date')[emotions_col],color=colors)


# happiness score chart

# using lag features because the future would be more related to the past day/2 days rather than average
# you could also add seasonal since it's more common than you would be happier over the weekend than weekday

st.subheader("Happiness Score Over Time")
new_df = df.copy()
new_df = new_df.sort_values('Date')
new_df['Lag_1'] = new_df['Happiness Score'].shift(1)
new_df['Lag_2'] = new_df['Happiness Score'].shift(2)
new_df['Lag_3'] = new_df['Happiness Score'].shift(3)
new_df = new_df.dropna()

X = new_df[['Lag_1', 'Lag_2', 'Lag_3']]
y = new_df["Happiness Score"]
# using 80/20 split, where test size is 20%
split = int(len(new_df) * 0.8)
X_train = X.iloc[:split]
X_test = X.iloc[split:]
y_train = y.iloc[:split]
y_test = y.iloc[split:]

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = pd.Series(model.predict(X_train), index=y_train.index)
y_fore = pd.Series(model.predict(X_test), index=y_test.index)

st.subheader("Time Series Forecast: Actual vs Predicted")
comparison = pd.DataFrame({
    'Actual': pd.concat([y_train, y_test]),
    'Train Predictions': pd.concat([pd.Series(y_pred, index=y_train.index), pd.Series([None]*len(y_test), index=y_test.index)]),
    'Test Predictions': pd.concat([pd.Series([None]*len(y_train), index=y_train.index), pd.Series(y_fore, index=y_test.index)])
})
st.line_chart(comparison.set_index(new_df['Date']))


col1, col2 = st.columns(2)
col1.metric("Train R²", f"{r2_score(y_train, y_pred):.3f}")
col2.metric("Test R²", f"{r2_score(y_test, y_fore):.3f}")

st.subheader("☁️ Tomorrow's Happiness Forecast")

# Get the most recent data point
last_row = new_df[['Lag_1', 'Lag_2', 'Lag_3']].iloc[-1:]

# Predict tomorrow
tomorrow_prediction = model.predict(last_row)[0]

# Display
st.metric(
    label="Predicted Happiness Score for Tomorrow",
    value=f"{tomorrow_prediction:.2f}",
    delta=f"{tomorrow_prediction - new_df['Happiness Score'].iloc[-1]:.2f} from yesterday ({new_df['Happiness Score'].iloc[-1]:.2f})"
)
