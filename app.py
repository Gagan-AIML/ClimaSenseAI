import streamlit as st
import pandas as pd
import requests

from streamlit_js_eval import get_geolocation
from api import get_coordinates, get_weather, get_air_quality, API_KEY
from disease_logic import map_specific_diseases
from ml_model import predict_health_impact_score as predict_health_impact
from email_service import send_alert_email, send_confirmation_email

# -------------------------------------------------
# Streamlit Config
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
# Session State
# -------------------------------------------------
if "risk_level" not in st.session_state:
    st.session_state.risk_level = None

if "diseases" not in st.session_state:
    st.session_state.diseases = []

# -------------------------------------------------
# Auto Location Detection (Browser Based)
# -------------------------------------------------
st.subheader("📍 Detecting Your Location")

geo_data = get_geolocation()

if geo_data:
    lat = geo_data["coords"]["latitude"]
    lon = geo_data["coords"]["longitude"]

    try:
        reverse_url = (
            f"http://api.openweathermap.org/geo/1.0/reverse"
            f"?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
        )
        reverse_response = requests.get(reverse_url).json()

        if reverse_response:
            city = reverse_response[0]["name"]
            st.success(f"Detected City: {city}")
        else:
            st.warning("City detection failed. Please enter manually.")
            city = st.text_input("Enter City Name")

    except:
        city = st.text_input("Enter City Name")

else:
    st.info("Please allow location access in your browser.")
    city = st.text_input("Enter City Name")

# -------------------------------------------------
# Health Risk Check
# -------------------------------------------------
if city and st.button("🔍 Check Health Risk"):
    try:
        lat, lon = get_coordinates(city)
        weather = get_weather(city)
        air = get_air_quality(lat, lon)

        diseases = map_specific_diseases(air, weather)

        # Predict Health Impact Score
        health_score = predict_health_impact(air, weather)

        # Risk classification
        if health_score >= 75 or len(diseases) >= 4:
            risk_level = "High"
        elif health_score >= 50 or len(diseases) >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        st.session_state.risk_level = risk_level
        st.session_state.diseases = diseases

        # ---------------- Display ----------------
        st.subheader("🌦 Environmental Conditions")
        st.write(f"🌡 Temperature: {weather['temperature']} °C")
        st.write(f"💧 Humidity: {weather['humidity']} %")
        st.write(f"🌧 Rainfall: {weather.get('rainfall', 0)} mm")
        st.write(f"🌫 AQI: {air['aqi']}")
        st.write(f"🌫 PM2.5: {air['pm25']}")
        st.write(f"🌫 PM10: {air['pm10']}")

        st.subheader("🏥 ML-Based Health Impact Score")
        st.write(f"Predicted Health Impact Score: **{health_score}**")

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

            send_confirmation_email(email, city)

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
