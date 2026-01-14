import smtplib
from email.mime.text import MIMEText

# -------------------------------------------------
# SMTP Configuration (Gmail)
# -------------------------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "yourgmail@gmail.com"
SENDER_PASSWORD = "your gmail password"  # App password

# -------------------------------------------------
# Core Email Sender
# -------------------------------------------------
def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# -------------------------------------------------
# Subscription Confirmation Email
# -------------------------------------------------
def send_confirmation_email(to_email, city):
    subject = "✅ ClimaSense Subscription Confirmed"

    body = f"""
Hello,

You have successfully subscribed to **ClimaSense AI** health alerts.

📍 Selected City: {city}

You will receive notifications whenever environmental conditions indicate a **MEDIUM or HIGH health risk** in your area.

This service provides **preventive health awareness** based on weather and air quality data.

Stay informed,
ClimaSense AI Team

⚠ This is not a medical diagnosis.
"""

    send_email(to_email, subject, body)

# -------------------------------------------------
# Health Risk Alert Email
# -------------------------------------------------
def send_alert_email(to_email, city, risk_level, diseases):
    subject = f"⚠ ClimaSense Health Alert – {city}"

    disease_text = (
        ", ".join(diseases)
        if diseases
        else "General environmental health stress"
    )

    body = f"""
Hello,

🚨 **ClimaSense has detected an increased health risk** in your area.

📍 City: {city}
⚠ Risk Level: {risk_level}

🦠 Possible Health Risks:
{disease_text}

🛡 Recommended Precautions:
• Limit outdoor exposure during peak hours
• Wear a mask if air quality is poor
• Stay hydrated and avoid heat stress
• Seek medical advice if symptoms appear

⚠ This alert is generated using environmental data
and does NOT replace professional medical consultation.

Stay safe,
ClimaSense AI Team
"""

    send_email(to_email, subject, body)
