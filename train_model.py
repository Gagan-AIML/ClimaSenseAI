import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import numpy as np

df = pd.read_csv("air_quality_health_impact_data.csv")

features = [
    "PM2_5", "PM10", "AQI",
    "Temperature", "Humidity",
    "NO2", "SO2", "O3"
]

X = df[features]
y = df["HealthImpactScore"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluation
print("R²:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

joblib.dump(model, "health_model.pkl")

print("✅ ML model trained & saved as health_model.pkl")
