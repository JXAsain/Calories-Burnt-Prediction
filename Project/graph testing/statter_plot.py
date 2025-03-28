
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

import warnings 


df = pd.read_csv('merged_data.csv')

df.describe()

features = ['Age', 'Height', 'Heart_Rate', 'Body_Temp']


plt.subplots(figsize=(15, 10))
for i, col in enumerate(features):
    plt.subplot(2, 2, i + 1)
    x = df.sample(1000)
    sb.scatterplot(x=col, y='Calories', data=x)
plt.tight_layout()
plt.show()