import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


class EmailService:
    def __init__(self):
        self.smtp_host = getattr(settings, "SMTP_HOST")
        self.smtp_port = getattr(settings, "SMTP_PORT")
        self.smtp_user = getattr(settings, "SMTP_USER")
        self.smtp_password = getattr(settings, "SMTP_PASSWORD")

    def send_email_with_attachment(self, to_email, subject, body, attachment, filename):
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with open(attachment.path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(filename))
        part["Content-Disposition"] = f'attachment; filename="{filename}"'
        msg.attach(part)

        try:
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
