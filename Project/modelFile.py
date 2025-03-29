import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings 
import pandas as pd
import matplotlib.pyplot as plt
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
        "Age": dict["age"],
        "Height": dict["height"],
        "Heart_Rate": dict["heart"],
        "Body_Temp": dict["bodytemp"],
        "Calories": dict["calories"] 
    }
    
    # Turns the merged data into a dataframe
    df = pd.read_csv('merged_data.csv')

    # Convert dictionary to DataFrame
    user_df = pd.DataFrame(user_data)
    # Features to analyze
    features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

    # Create subplots
    plt.figure(figsize=(15, 10))

    for i, col in enumerate(features):
        plt.subplot(2, 2, i + 1)
        
        # Plot histogram with KDE for the original dataset
        sb.histplot(df[col], kde=True, bins=30, color='blue', label='Others', alpha=0.6)
        
        # Overlay dictionary data as vertical lines
        for value in user_df[col]:
            plt.axvline(x=value, color='red', linestyle='dashed', linewidth=2, label='You' if value == user_df[col].iloc[0] else "")

        # Titles and labels
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Density')

    plt.tight_layout()
    plt.legend()
    plt.show()

# uses the user input to put them into a histogram of our data
def userdata_compare_statter(dict):

    # Converts the apps dict style and adds calories value to the dict
    user_data = {
        "Age": dict["age"],
        "Height": dict["height"],
        "Heart_Rate": dict["heart"],
        "Body_Temp": dict["bodytemp"],
        "Calories": dict["calories"] 
    }
    
    # Turns the merged data into a dataframe
    df = pd.read_csv('merged_data.csv')

    # Convert dictionary to DataFrame
    user_df = pd.DataFrame(user_data)
        
    # Features to analyze
    features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

    # Create subplots
    plt.figure(figsize=(15, 10))

    for i, col in enumerate(features):
        plt.subplot(2, 2, i + 1)
        
        # Sample data for readability
        x1 = df.sample(1000)  

        # Plot original dataset
        sb.scatterplot(x=x1[col], y=x1['Calories'], color='blue', label='1000 Others', alpha=0.5)
        
        # Overlay new list-based data
        sb.scatterplot(x=user_df[col], y=user_df['Calories'], color='red', label='You', marker='D', s=100)

        # Titles and labels
        plt.title(f'Scatter Plot of {col} vs Calories Burned')
        plt.xlabel(col)
        plt.ylabel('Calories Burned')

    plt.tight_layout()
    plt.legend()
    plt.show()


def received_csv_data_histogram(csv):
    try:
        # Turns the revieced data into a dataframe
        df = pd.read_csv(csv)

        # Features to analyze
        features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

        # Create subplots for normal distribution visualization
        plt.figure(figsize=(15, 10))

        for i, col in enumerate(features):
            plt.subplot(2, 2, i + 1)
            
            # Plot histogram with KDE (smooth curve to approximate normal distribution)
            sb.histplot(df[col], kde=True, bins=30, color='blue', alpha=0.6)
            
            # Titles and labels
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Density')

        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Error: The CSV file was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an error parsing the CSV file. Ensure it is properly formatted.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def received_csv_data_scatter(csv):
    try:
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
        plt.figure(figsize=(15, 10))

        for i, col in enumerate(required_columns[:-1]):  # Excluding 'Calories' from x-axis features
            plt.subplot(2, 2, i + 1)
            
            # Sample data for readability
            x1 = df.sample(min(1000, len(df)))  # Ensure sampling doesn't exceed available rows

            # Plot scatter plot
            sb.scatterplot(x=x1[col], y=x1['Calories'], color='blue', alpha=0.5)

            # Titles and labels
            plt.title(f'Scatter Plot of {col} vs Calories Burned')
            plt.xlabel(col)
            plt.ylabel('Calories Burned')

        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Error: The CSV file was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an error parsing the CSV file. Ensure it is properly formatted.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


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
    
    #print(f"✅ Predictions saved to {output_csv}")
