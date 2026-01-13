import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("air_quality_health_impact_data.csv")

features = [
    "PM2_5", "PM10", "AQI",
    "Temperature", "Humidity"
]

X = df[features]
y = df["HospitalAdmissions"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    objective="reg:squarederror"
)

model.fit(X_train, y_train)

joblib.dump(model, "health_model.pkl")

print("✅ ML model trained & saved as health_model.pkl")
