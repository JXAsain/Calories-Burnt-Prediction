import streamlit as st
import requests

st.title("🔥Calorie Burnt Prediction App🔥")

# User input fields
weight = st.number_input("Weight (lb): ", min_value=0.0, max_value=0.0, step=0.1)
age = st.number_input("Age: ", min_value=0, max_value=0, step=1)
gender = st.selectbox("Gender", ["Select", "Male", "Female"])
rate = st.number_input("Heart Rate💓(bpm): ", min_value=0, max_value=0, step=1)
duration = st.number_input("Workout Duration💦(min): ", min_value=0, max_value=0, step=1)

# Button to send data to backend API
if st.button("🚨 CALORIE PREDICTION"):
    userData = {
        "weight": weight,
        "age": age,
        "gender": gender,
        "heart": rate,
        "workout": duration
    }
    response = requests.post("http://127.0.0.1:5000/predict", json=userData)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"🔥Estimated Calories Burnt: {result['caloriesBurnt']} lb🔥")
    else:
        st.error("⚠️Error: Failed to retrieve your prediction.⚠️")
