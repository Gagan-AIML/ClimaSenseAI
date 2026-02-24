import joblib
import numpy as np

# Load trained model
model = joblib.load("health_model.pkl")

def predict_health_impact_score(air, weather):
    """
    Predict Health Impact Score using live air & weather data.
    Feature order MUST match training.
    """

    features = np.array([[  
        air["pm25"],              
        air["pm10"],              
        air["aqi"],               
        weather["temperature"],   
        weather["humidity"],      
        air["no2"],               
        air["so2"],               
        air["o3"]                 
    ]])

    prediction = model.predict(features)[0]

    return round(float(prediction), 2)