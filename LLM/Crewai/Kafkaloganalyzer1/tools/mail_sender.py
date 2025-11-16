import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

@tool
def email_sender_tool(body: str, subject: str = "Kafka Log Analysis Report") -> str:
    """
    Sends email with the Kafka analysis summary using a body and optional subject line.
    """
    try:
        msg = MIMEText(body) # Use only the body here for content
        msg["Subject"] = subject # Set the actual email subject line
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = os.getenv("SEND_TO")

        server = smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")))
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.sendmail(os.getenv("EMAIL_USER"), os.getenv("SEND_TO"), msg.as_string())
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        print(f"DEBUG: Email error details: {e}")
        return f"Email error: {e}"
