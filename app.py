import streamlit as st
from api import get_coordinates, get_weather, get_air_quality
from email_service import send_alert_email

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="  ClimaSense AI",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️  ClimaSense AI")
st.caption("Climate-Based Disease Risk Sensing & Alert System")

st.markdown("""
 ClimaSense AI senses **environmental conditions** and identifies
**possible disease risks** associated with climate and air quality.

⚠ This system provides **preventive risk alerts**, not medical diagnosis.
""")

# --------------------------------------------------
# City selection
# --------------------------------------------------
cities = [
    "Delhi", "Mumbai", "Pune", "Bengaluru", "Chennai", "Hyderabad",
    "Kochi", "Thiruvananthapuram", "Coimbatore", "Madurai",
    "Ahmedabad", "Surat", "Nagpur", "Panaji",
    "Guwahati", "Shillong", "Imphal", "Itanagar",
    "Jammu", "Srinagar", "Dehradun", "Shimla"
]

city = st.selectbox("🌍 Select City", cities)

email = st.text_input("📧 Enter your email to receive alert")

# --------------------------------------------------
# Disease risk logic (NO ML)
# --------------------------------------------------
def assess_health_risk(air, weather):
    diseases = []

    # Air pollution related
    if air["pm25"] > 100 or air["aqi"] >= 4:
        diseases += ["Asthma", "COPD", "Bronchitis"]

    # Seasonal influenza
    if weather["temperature"] < 18 and weather["humidity"] > 60:
        diseases += ["Influenza", "Pneumonia"]

    # Heat stress
    if weather["temperature"] >= 38:
        diseases += ["Heat Exhaustion", "Dehydration"]

    # High humidity / monsoon
    if weather["humidity"] > 75:
        diseases += ["Skin Infection Risk"]

    # Overall risk level
    if len(diseases) >= 3:
        risk_level = "High"
    elif len(diseases) >= 1:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_level, list(set(diseases))

# --------------------------------------------------
# Action button
# --------------------------------------------------
if st.button("🔍 Check Health Risk & Send Alert"):
    try:
        lat, lon = get_coordinates(city)
        weather = get_weather(city)
        air = get_air_quality(lat, lon)

        risk_level, diseases = assess_health_risk(air, weather)

        # ---------------- Display environment ----------------
        st.subheader("🌦 Environmental Conditions")
        st.write(f"🌡 Temperature: {weather['temperature']} °C")
        st.write(f"💧 Humidity: {weather['humidity']} %")
        st.write(f"🌫 AQI: {air['aqi']}")
        st.write(f"🌫 PM2.5: {air['pm25']}")
        st.write(f"🌫 PM10: {air['pm10']}")

        # ---------------- Display risk ----------------
        st.subheader("⚠ Health Risk Assessment")
        if risk_level == "High":
            st.error("HIGH RISK")
        elif risk_level == "Medium":
            st.warning("MEDIUM RISK")
        else:
            st.success("LOW RISK")

        st.subheader("🦠 Possible Disease Risks")
        if diseases:
            for d in diseases:
                st.write("•", d)
        else:
            st.write("No significant disease risk detected.")

        # ---------------- Email alert ----------------
        if email:
            if risk_level in ["Medium", "High"]:
                send_alert_email(email, city, risk_level, diseases)
                st.success("📩 Alert email sent successfully!")
            else:
                st.info("Risk is low. No alert email sent.")

        else:
            st.warning("Enter email to receive alert.")

    except Exception as e:
        st.error("Unable to fetch data or send alert.")
        st.text(str(e))

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption(
    "⚠ Disclaimer:  ClimaSense AI provides environmental health risk awareness only "
    "and does not replace professional medical advice."
)
