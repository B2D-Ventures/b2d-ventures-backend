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

    def send_email_with_attachment(self, to_email, subject, body, attachment=None, filename=None):
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP user and password must be set in the settings.")

        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if attachment and filename:
            with open(attachment.path, "rb") as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(filename))
            part["Content-Disposition"] = f'attachment; filename="{filename}"'
            msg.attach(part)

        try:
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def build_deal_notification_content(deal, action, custom_message=None):
        """Build the subject and body for a deal notification email."""
        subject = f"Deal Update: {deal.name}"
        body = f"Dear {deal.startup.username},\n\n"

        if action == "approved":
            body += f"Your deal '{deal.name}' has been approved. Congratulations! Your deal is now live on our platform."
        elif action == "rejected":
            body += f"Your deal '{deal.name}' has been rejected. We apologize for any inconvenience. If you have any questions, please contact our support team."
        elif custom_message:
            body += custom_message
        else:
            body += f"There has been an update regarding your deal '{deal.name}'."

        body += "\n\nBest regards,\nThe B2D Ventures Team"

        return subject, body
