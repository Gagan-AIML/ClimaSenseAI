import joblib
import numpy as np

# Load trained model
model = joblib.load("health_model.pkl")

def predict_hospital_admissions(air, weather):
    """
    Predict respiratory case burden using live air & weather data.
    Feature order MUST match training.
    """

    features = np.array([[
        air["pm25"],        # PM2_5
        air["pm10"],        # PM10
        air["aqi"],         # AQI
        weather["temperature"],  # Temperature
        weather["humidity"],     # Humidity
        air["no2"],         # NO2
        air["so2"],         # SO2
        air["o3"]           # O3
    ]])

    prediction_log = model.predict(features)[0]

    # reverse log1p transform
    prediction = np.expm1(prediction_log)

    return max(0, int(round(prediction)))
