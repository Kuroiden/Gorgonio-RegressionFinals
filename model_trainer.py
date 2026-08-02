import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataframe = pd.read_csv("battery_health_dataset.csv")

x = dataframe[['Battery Age', 'Daily Usage Hours', 'Gaming User', 'Design Capacity', 'Cycle Count', 'CPU Usage', 'GPU Usage', 'Power Consumption', 'Average Temperature']]
y = dataframe['Full Charge Capacity']

train_x, test_x, train_y, test_y = train_test_split(
    x, y, test_size=0.1, train_size=0.35
)

regression_model = LinearRegression()
regression_model.fit(train_x, train_y)

joblib.dump(regression_model, "batthealth.pkl")
print("Trained data model generation attempted. Check if the file exists.")