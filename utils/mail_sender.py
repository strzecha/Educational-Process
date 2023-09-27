from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl

from utils.data_reader import get_properties

properties = get_properties()
credentials_filename = properties.get("CREDENTIALS_FILE").data
credentials = get_properties(credentials_filename)

EMAIL_SENDER = credentials.get("EMAIL_SENDER").data
EMAIL_PASSWORD = credentials.get("EMAIL_PASSWORD").data
EMAIL_RECEIVER = credentials.get("EMAIL_RECEIVER").data
USERNAME = credentials.get("USERNAME").data

class MailSender:
    def __init__(self):
        self.email_sender = EMAIL_SENDER
        self.email_password = EMAIL_PASSWORD
        self.email_receiver = EMAIL_RECEIVER
        self.username = USERNAME

    def create_mail(self, message):
        subject = f"Wyniki użytkownika {self.username}"
        body = f"""
                <!doctype html>
                <html lang="pl">
                <head></head>
                <body>
                    <p>{message}</p>
                </body>
                </html>"""

        self.mail = MIMEMultipart("alternative")

        self.mail['From'] = self.email_sender
        self.mail['To'] = self.email_receiver
        self.mail['Subject'] = subject
        part = MIMEText(body, 'html')

        self.mail.attach(part)

    def send_mail(self):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, self.email_receiver, self.mail.as_string())
