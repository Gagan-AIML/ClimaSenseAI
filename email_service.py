import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "climasenseai@gmail.com"
SENDER_PASSWORD = "uxcz zrog xmaj laqy"  # Gmail App Password

def send_alert_email(to_email, city, risk_level, diseases):
    subject = f"Health Alert for {city}"

    body = f"""
Hello,

ClimaSense has detected an increased health risk for your location.

City: {city}
Risk Level: {risk_level}

Possible Health Risks:
{', '.join(diseases) if diseases else 'General environmental stress'}

Precautionary Measures:
• Limit outdoor exposure
• Wear a mask if air quality is poor
• Stay hydrated
• Seek medical advice if symptoms appear

⚠ This is a preventive alert based on environmental conditions,
not a medical diagnosis.

Stay Safe,
ClimaSense AI Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
