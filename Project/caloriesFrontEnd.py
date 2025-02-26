import streamlit as st
import requests

st.title("🔥Calorie Burnt Prediction App🔥")

# User input fields
age = st.number_input("Age: ", min_value=0, max_value=200, step=1)
gender = st.selectbox("Gender", ["Select", "Male", "Female"])
height = st.number_input("Height📏(cm): ", min_value=0, max_value=400, step=1)
rate = st.number_input("Heart Rate💓(bpm): ", min_value=0, max_value=300, step=1)
intensity = st.number_input("Body Temperature🌡️(C): ", min_value=0.0, max_value=50.0, step=0.1)

# Button to send data to backend API
if st.button("🚨 CALORIE PREDICTION"):
    userData = {
        "age": age,
        "gender": gender,
        "height": height,
        "heart": rate,
        "bodyTemp": intensity
    }
    response = requests.post("http://127.0.0.1:5000/predict", json=userData)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"🔥Estimated Calories Burnt: {result['caloriesBurnt']} lb🔥")
    else:
        st.error("⚠️Error: Failed to retrieve your prediction.⚠️")
