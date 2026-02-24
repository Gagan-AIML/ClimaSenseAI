import numpy as np
import xgboost as xgb

# Load booster directly
booster = xgb.Booster()
booster.load_model("health_model.json")

def predict_health_impact_score(air, weather):
    import numpy as np
import xgboost as xgb

# Load booster directly
booster = xgb.Booster()
booster.load_model("health_model.json")

def predict_health_impact_score(air, weather):
    features = np.array([[
        air["pm2_5"],
        air["pm10"],
        air["aqi"],
        weather["temperature"],
        weather["humidity"],
        air["no2"],
        air["so2"],
        air["o3"]
    ]])

    dmatrix = xgb.DMatrix(features)
    prediction = booster.predict(dmatrix)

    return float(prediction[0])

    dmatrix = xgb.DMatrix(features)
    prediction = booster.predict(dmatrix)

    return float(prediction[0])