import numpy as np
from xgboost import XGBRegressor

# 1. Initialize the shell
model = XGBRegressor()

# 2. THE CRITICAL FIX: Manually define the estimator type
# This satisfies the internal check in the load_model function
model._estimator_type = "regressor" 

# 3. Load your file (This will no longer crash!)
model.load_model("health_model.json")

def predict_health_impact_score(air, weather):
    """
    Predict Health Impact Score using live air & weather data.
    Feature order MUST match training.
    """
    try:
        features = np.array([[  
            air.get("pm25", 0),         
            air.get("pm10", 0),         
            air.get("aqi", 0),                
            weather.get("temperature", 0),   
            weather.get("humidity", 0),      
            air.get("no2", 0),                
            air.get("so2", 0),                
            air.get("o3", 0)                  
        ]])

        prediction = model.predict(features)[0]
        return round(float(prediction), 2)
        
    except Exception as e:
        # Returns 0.0 if there is an error fetching a specific pollutant
        return 0.0