import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv('merged_data.csv')

# Features to analyze
features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']

# Create subplots for normal distribution visualization
plt.figure(figsize=(15, 10))

for i, col in enumerate(features):
    plt.subplot(2, 2, i + 1)
    
    # Plot histogram with KDE (smooth curve to approximate normal distribution)
    sb.histplot(df[col], kde=True, bins=30, color='blue')
    
    # Titles and labels
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Density')

plt.tight_layout()
plt.show()
