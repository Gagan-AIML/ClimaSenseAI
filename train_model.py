import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

df = pd.read_csv("air_quality_health_impact_data.csv")

# Feature engineering


features = [
    "PM2_5", "PM10", "AQI",
    "Temperature", "Humidity",
    "NO2","SO2","O3"
]

X = df[features]
y = np.log1p(df["RespiratoryCases"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = np.expm1(model.predict(X_test))

joblib.dump(model, "health_model.pkl")

print("✅ ML model trained & saved as health_model.pkl")
