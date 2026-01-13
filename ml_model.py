import joblib
import numpy as np

model = joblib.load("health_model.pkl")

def predict_hospital_admissions(air, weather):
    features = np.array([[
        air["pm25"],
        air["pm10"],
        air["aqi"],
        weather["temperature"],
        weather["humidity"]
    ]])

    prediction = model.predict(features)[0]
    return max(int(prediction), 0)
