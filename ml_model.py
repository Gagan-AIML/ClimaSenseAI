import numpy as np

# Load trained model
from xgboost import XGBRegressor

model = XGBRegressor()
model.load_model("health_model.json")

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