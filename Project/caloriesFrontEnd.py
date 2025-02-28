import streamlit as st
import requests
import modelFile

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

    # Double checks a expected gender was selected
    if gender == "Select":
        st.error("⚠️ Please select a valid gender ⚠️")
    else:
        userData["Gender"] = gender
        
        try:
            # Calls modelFile to run prediction
            predictedCalories = modelFile.run(userData)
            st.success(f"🔥Estimated Calories Burnt: {predictedCalories[0]:.2f} kcal🔥")
        
        except Exception:
            # Output message should system fails
            st.error("⚠️ Failed to retrieve your prediction ⚠️")
