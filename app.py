import streamlit as st
import pandas as pd
import requests

from api import get_coordinates, get_weather, get_air_quality, get_weather_air_by_city
from disease_logic import map_specific_diseases
from ml_model import predict_hospital_admissions as predict_hospital_cases
from email_service import send_alert_email, send_confirmation_email

# -------------------------------------------------
# Streamlit Session State Initialization
# -------------------------------------------------
if "risk_level" not in st.session_state:
    st.session_state.risk_level = None

if "diseases" not in st.session_state:
    st.session_state.diseases = []

# -------------------------------------------------
# IP-Based Location Detection
# -------------------------------------------------
def get_city_from_ip():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        return response.json().get("city")
    except:
        return None

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="ClimaSense AI",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 ClimaSense AI")
st.caption("Climate-Driven Health Risk Alert System (Non-Diagnostic)")

st.markdown("""
This system provides **preventive health risk alerts** based on real-time
weather and air quality conditions.
""")

# -------------------------------------------------
# Location Selection
# -------------------------------------------------
cities = [
    "Delhi", "Mumbai", "Pune", "Bengaluru", "Chennai", "Hyderabad",
    "Kochi", "Thiruvananthapuram", "Coimbatore", "Madurai",
    "Ahmedabad", "Surat", "Nagpur", "Panaji",
    "Guwahati", "Shillong", "Imphal", "Itanagar",
    "Jammu", "Srinagar", "Dehradun", "Shimla"
]

detected_city = get_city_from_ip()
use_current = st.checkbox("📍 Use current location", value=True)

if use_current and detected_city in cities:
    city = detected_city
    st.info(f"Detected City: {city}")
else:
    city = st.selectbox("🌍 Select City", cities)

# -------------------------------------------------
# Health Risk Check
# -------------------------------------------------
if st.button("🔍 Check Health Risk"):
    try:
        lat, lon = get_coordinates(city)
        weather = get_weather(city)
        air = get_air_quality(lat, lon)

        diseases = map_specific_diseases(air, weather)
        predicted_cases = predict_hospital_cases(air, weather)

        # Risk fusion logic
        if predicted_cases >= 15 or len(diseases) >= 4:
            risk_level = "High"
        elif predicted_cases >= 7 or len(diseases) >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Save to session state
        st.session_state.risk_level = risk_level
        st.session_state.diseases = diseases

        # ---------------- Display ----------------
        st.subheader("🌦 Environmental Conditions")
        st.write(f"🌡 Temperature: {weather['temperature']} °C")
        st.write(f"💧 Humidity: {weather['humidity']} %")
        st.write(f"🌧 Rainfall: {weather['rainfall']} mm")
        st.write(f"🌫 AQI: {air['aqi']}")
        st.write(f"🌫 PM2.5: {air['pm25']}")
        st.write(f"🌫 PM10: {air['pm10']}")

        st.subheader("🏥 ML-Based Respiratory Risk Indicator")
        st.write(f"Predicted Respiratory Cases: **{predicted_cases}**")

        st.subheader("⚠ Health Risk Assessment")
        if risk_level == "High":
            st.error("🚨 HIGH RISK")
        elif risk_level == "Medium":
            st.warning("⚠️ MEDIUM RISK")
        else:
            st.success("✅ LOW RISK")

        st.subheader("🦠 Likely Disease Risks")
        if diseases:
            for d in diseases[:3]:
                st.write("•", d)
        else:
            st.write("No major health risks detected")

    except Exception as e:
        st.error("Unable to fetch data for this city.")
        st.text(str(e))

# -------------------------------------------------
# Subscription Section
# -------------------------------------------------
st.divider()
st.subheader("📬 Subscribe for Health Alerts")

email = st.text_input("Enter your email address")

if st.button("🔔 Subscribe for Alerts"):
    if not email:
        st.error("Please enter a valid email address.")
    elif st.session_state.risk_level is None:
        st.warning("Please check health risk before subscribing.")
    else:
        try:
            df = pd.read_csv("subscribers.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["email", "city"])

        if not ((df["email"] == email) & (df["city"] == city)).any():
            df.loc[len(df)] = [email, city]
            df.to_csv("subscribers.csv", index=False)

            # ✅ ALWAYS send confirmation email
            send_confirmation_email(email, city)

            # ⚠️ Send alert email ONLY if risk is Medium or High
            if st.session_state.risk_level in ["Medium", "High"]:
                send_alert_email(
                    email,
                    city,
                    st.session_state.risk_level,
                    st.session_state.diseases
                )

            st.success("✅ Subscription successful! Emails sent.")
        else:
            st.info("ℹ️ You are already subscribed for this city.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption(
    "⚠ Disclaimer: ClimaSense AI provides environmental health risk awareness only "
    "and does not replace professional medical advice."
)
