import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings 
import pandas as pd
from matplotlib.figure import Figure
import seaborn as sb


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

    # Add predicted_calories to the dictionary
    dict['calories'] = predicted_calories

    print(f"Predicted Calories: {predicted_calories[0]:.2f}")
    return predicted_calories


def percentile(attr, value):
    dataframe = pd.read_csv('merged_data.csv')
    data = dataframe[attr]
    sorted = np.sort(data)

    rank = (sorted < value).sum() 
    
    percentile = (rank / len(sorted)) * 100
    percentile = round(percentile, 2)
    return percentile

# uses the user input to put them into a histogram of our data
def userdata_compare_histogram(dict):
    # Converts the apps dict style and adds calories value to the dict
    user_data = {
        "Age": [dict["age"]],
        "Height": [dict["height"]],
        "Heart_Rate": [dict["heart"]],
        "Body_Temp": [dict["bodyTemp"]],
        "Calories": [dict["calories"]]
    }
    
    # Turns the merged data into a dataframe
    df = pd.read_csv('merged_data.csv')

    # Convert dictionary to DataFrame
    user_df = pd.DataFrame(user_data)
    # Features to analyze
    features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

    # Create subplots
    fig = Figure(figsize=(10, 8))
    axes = fig.subplots(2, 2)

    for i, col in enumerate(features):
        ax = axes[i // 2, i % 2]

        # Plot histogram with KDE for the original dataset
        sb.histplot(df[col], kde=True, bins=30, color='blue', label='Others', alpha=0.6, ax=ax)
        
        # Overlay dictionary data as vertical lines
        for value in user_df[col]:
            ax.axvline(x=value, color='red', linestyle='dashed', linewidth=2, label='You' if value == user_df[col].iloc[0] else "")

        # Titles and labels
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Density')
        ax.legend()

    fig.tight_layout()
    return fig


# uses the user input to put them into a histogram of our data
def userdata_compare_statter(dict):

    # Converts the apps dict style and adds calories value to the dict
    user_data = {
        "Age": [dict["age"]],
        "Height": [dict["height"]],
        "Heart_Rate": [dict["heart"]],
        "Body_Temp": [dict["bodyTemp"]],
        "Calories": [dict["calories"]]
    }    
    # Turns the merged data into a dataframe
    df = pd.read_csv('merged_data.csv')

    # Convert dictionary to DataFrame
    user_df = pd.DataFrame(user_data)
        
    # Features to analyze
    features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

    # Create subplots
    fig = Figure(figsize=(10, 8))
    axes = fig.subplots(2, 2)

    for i, col in enumerate(features):
        ax = axes[i // 2, i % 2]
        
        # Sample data for readability
        x1 = df.sample(1000)  

        # Plot original dataset
        sb.scatterplot(x=x1[col], y=x1['Calories'], color='blue', label='1000 Others', alpha=0.5, ax=ax)
        
        # Overlay new list-based data
        sb.scatterplot(x=user_df[col], y=user_df['Calories'], color='red', label='You', marker='D', s=100, ax=ax)

        # Titles and labels
        ax.set_title(f'Scatter Plot of {col} vs Calories Burned')
        ax.set_xlabel(col)
        ax.set_ylabel('Calories Burned')
        ax.legend()

    fig.tight_layout()
    return fig

# Generates histogram from CSV file
def received_csv_data_histogram(csv):

    # Turns the revieced data into a dataframe
    df = pd.read_csv(csv)

    # Features to analyze
    features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

    # Create subplots for normal distribution visualization
    fig = Figure(figsize=(10, 8))
    axes = fig.subplots(2, 2)

    for i, col in enumerate(features):
        ax = axes[i // 2, i % 2]
        
        # Plot histogram with KDE (smooth curve to approximate normal distribution)
        sb.histplot(df[col], kde=True, bins=30, color='blue', alpha=0.6, ax=ax)
        
        # Titles and labels
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Density')

    fig.tight_layout()
    return fig

# Generates scatter plot from CSV file
def received_csv_data_scatter(csv):
    # Load CSV file
    df = pd.read_csv(csv)

    # Required features
    required_columns = ['Age', 'Height', 'Heart_Rate', 'Body_Temp', 'Calories']
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {', '.join(missing_columns)}")

    # Check if there are missing values in the required columns
    if df[required_columns].isnull().values.any():
        raise ValueError("CSV contains missing values in required columns.")

    # Create subplots
    fig = Figure(figsize=(10, 8))
    axes = fig.subplots(2, 2)

    for i, col in enumerate(required_columns[:-1]):  # Excluding 'Calories' from x-axis features
        ax = axes[i // 2, i % 2]
        
        # Sample data for readability
        x1 = df.sample(min(1000, len(df)))  # Ensure sampling doesn't exceed available rows

        # Plot scatter plot
        sb.scatterplot(x=x1[col], y=x1['Calories'], color='blue', alpha=0.5,ax=ax)

        # Titles and labels
        ax.set_title(f'Scatter Plot of {col} vs Calories Burned')
        ax.set_xlabel(col)
        ax.set_ylabel('Calories Burned')

    fig.tight_layout()
    return fig


def predict_and_save_csv(input_csv, output_csv):
    warnings.filterwarnings('ignore')

    # Load the trained model and scaler
    loaded_model = joblib.load('calories_predictor.pkl')
    scaler = joblib.load('scaler.pkl')

    # Load the input CSV file
    df = pd.read_csv(input_csv)

    # Ensure required columns exist
    required_columns = ['Gender', 'Age', 'Height', 'Heart_Rate', 'Body_Temp']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {', '.join(missing_columns)}")

    # Convert Gender column to numerical (0 = Male, 1 = Female)
    df['Gender'] = df['Gender'].apply(lambda x: 0 if x.lower() == 'male' else 1)

    # Select features for prediction
    features = ['Gender', 'Age', 'Height', 'Heart_Rate', 'Body_Temp']
    input_data = df[features].values

    # Scale input data
    input_data = scaler.transform(input_data)

    # Predict Calories
    df['Calories'] = loaded_model.predict(input_data)

    # Save the new CSV with the predicted Calories column
    df.to_csv(output_csv, index=False)
    