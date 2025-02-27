import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

import warnings 

def run(dict):
    warnings.filterwarnings('ignore')

    # Load the trained model
    loaded_model = joblib.load('calories_predictor.pkl')
    scaler = joblib.load('scaler.pkl')
    if dict['gender'] == 'Male':
        gender = 0
    else:
        gender = 1
    age = dict['age']
    height = dict['height']
    heart_rate = dict['heart']
    body_temp = dict['bodyTemp']
    sample_input = np.array([[gender, age, height, heart_rate, body_temp]])  # Genger, Age, Height, heart rate, body temp
    
    # Normalize the input
    sample_input = scaler.transform(sample_input)
    
    # Make a prediction
    predicted_calories = loaded_model.predict(sample_input)
    print(f"Predicted Calories: {predicted_calories[0]:.2f}")
    return predicted_calories