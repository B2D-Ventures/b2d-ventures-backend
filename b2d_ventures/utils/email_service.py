import os
import smtplib
from decimal import Decimal

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

    def send_email_with_attachment(
        self, to_email, subject, body, attachment=None, filename=None
    ):
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

    @staticmethod
    def build_investment_notification_content(investment, recipient_type):
        """Build the subject and body for an investment notification email."""
        deal = investment.deal
        investor = investment.investor
        investment_amount = investment.investment_amount
        platform_fee = investment_amount * Decimal("0.03")
        net_investment = investment_amount - platform_fee

        if recipient_type == "investor":
            subject = f"Investment Confirmation: {deal.name}"
            body = f"""
                Dear {investor.username},

                Your investment of ${investment_amount} in {deal.name} has been successfully processed.

                Investment details:
                - Deal: {deal.name}
                - Amount: ${investment_amount}
                - Platform fee: ${platform_fee}
                - Net investment: ${net_investment}

                Thank you for your investment!

                Best regards,
                The B2D Ventures Team
                """
        elif recipient_type == "startup":
            subject = f"New Investment Received: {deal.name}"
            body = f"""
                Dear {deal.startup.username},

                Great news! Your deal {deal.name} has received a new investment.

                Investment details:
                - Amount: ${net_investment} (after platform fee)
                - Total amount_raised: ${deal.amount_raised}
                - Total investors: {deal.investor_count}

                Congratulations on your progress!

                Best regards,
                The B2D Ventures Team
                """
        else:
            raise ValueError("Invalid recipient_type. Must be 'investor' or 'startup'.")

        return subject, body
