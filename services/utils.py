from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.settings import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def send_email(subject, content, recipients):
    msg = MIMEMultipart()
    msg['From'] = settings.SENDER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Erreur lors de l'envoi de l'e-mail:", e)
        raise

