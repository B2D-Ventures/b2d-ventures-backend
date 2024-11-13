"""The module defines the InvestorService class and InvestorError."""

from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from b2d_ventures.app.models import Investor, Deal, Investment, Startup, Meeting
from b2d_ventures.app.serializers import (
    InvestorSerializer,
    InvestmentSerializer,
    MeetingSerializer,
)
from b2d_ventures.app.services import AuthService
from b2d_ventures.app.services.calendar_service import CalendarService, CalendarError
from b2d_ventures.utils import EmailService


class InvestorError(Exception):
    """Custom Exception for investor-related errors."""


class InvestorService:
    """Class definition for InvestorService."""

    @staticmethod
    def get_profile(pk):
        """Get investor's profile."""
        try:
            investor = Investor.objects.get(id=pk)
            serializer = InvestorSerializer(investor)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Exception as e:
            raise InvestorError(f"Error getting investor profile: {str(e)}")

    @staticmethod
    def list_investments(pk):
        """List investments made by the investor."""
        try:
            investor = Investor.objects.get(id=pk)
            investments = Investment.objects.filter(investor=investor)
            serializer = InvestmentSerializer(investments, many=True)
            response_data = [
                {"attributes": investment_data} for investment_data in serializer.data
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Exception as e:
            raise InvestorError(f"Error listing investments: {str(e)}")

    @staticmethod
    @transaction.atomic
    def create_investment(pk, deal_id, attributes):
        """Create a new investment."""
        try:
            investor = Investor.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id, status="approved")
            investment_amount = Decimal(attributes.get("investment_amount"))

            if investment_amount < deal.minimum_investment:
                raise InvestorError(
                    f"The minimum investment amount for this deal is ${deal.minimum_investment}"
                )

            platform_fee = investment_amount * Decimal("0.03")
            net_investment = investment_amount - platform_fee

            investor.total_invested += investment_amount
            investor.save()

            deal.startup.total_raised += net_investment
            deal.startup.save()

            deal.amount_raised += net_investment
            deal.investor_count += 1
            deal.save()

            investment = Investment.objects.create(
                deal=deal, investor=investor, investment_amount=investment_amount
            )

            email_service = EmailService()

            investor_subject, investor_body = (
                email_service.build_investment_notification_content(
                    investment, "investor"
                )
            )
            email_service.send_email_with_attachment(
                to_email=investor.email, subject=investor_subject, body=investor_body
            )

            startup_subject, startup_body = (
                email_service.build_investment_notification_content(
                    investment, "startup"
                )
            )
            email_service.send_email_with_attachment(
                to_email=deal.startup.email, subject=startup_subject, body=startup_body
            )

            serializer = InvestmentSerializer(investment)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except InvestorError as e:
            raise InvestorError(str(e))
        except PermissionDenied as e:
            raise PermissionDenied(str(e))
        except Exception as e:
            raise InvestorError(f"Error creating investment: {str(e)}")

    @staticmethod
    def get_investment(pk, investment_id):
        """Get details of a specific investment."""
        try:
            investor = Investor.objects.get(id=pk)
            investment = Investment.objects.get(id=investment_id, investor=investor)
            serializer = InvestmentSerializer(investment)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Investment.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Investment with id {investment_id} does not exist for this investor"
            )
        except Exception as e:
            raise InvestorError(f"Error getting investment details: {str(e)}")

    @staticmethod
    def request_dataroom(pk, deal_id):
        """Request access to a deal's dataroom and send it via email."""
        try:
            investor = Investor.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id)

            if not deal.dataroom:
                raise InvestorError("No dataroom file available for this deal.")

            investor_email = investor.email
            dataroom_url = deal.dataroom.url

            email_service = EmailService()
            email_subject = f"Dataroom Access for {deal.name}"
            email_body = (
                f"Dear {investor.username},\n\n"
                f"You have requested access to the dataroom for the deal: {deal.name}.\n"
                f"Please download the file using the following link:\n\n"
                f"{dataroom_url}\n\n"
                f"Best regards,\nThe Team"
            )

            email_service.send_email_with_attachment(
                to_email=investor_email,
                subject=email_subject,
                body=email_body,
            )

            return Response(
                {"message": "Dataroom sent successfully to your email"},
                status=status.HTTP_200_OK,
            )
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except InvestorError as e:
            raise InvestorError(str(e))
        except Exception as e:
            raise InvestorError(f"Error sending dataroom: {str(e)}")

    @staticmethod
    def schedule_meeting(investor_id, startup_id, attributes):
        try:
            investor = Investor.objects.get(id=investor_id)
            startup = Startup.objects.get(id=startup_id)

            start_time = datetime.fromisoformat(attributes.get("start_time"))
            end_time = datetime.fromisoformat(attributes.get("end_time"))
            title = attributes.get("title", "Investor-Startup Meeting")
            description = attributes.get("description", "")

            refresh_token = investor.refresh_token
            if not refresh_token:
                raise InvestorError("Investor does not have a valid refresh token")

            auth_service = AuthService()
            access_token = auth_service.refresh_access_token(refresh_token)

            event = CalendarService.schedule_investor_startup_meeting(
                access_token, title, description, start_time, end_time, startup.email
            )

            meeting = Meeting.objects.create(
                investor=investor,
                startup=startup,
                start_time=start_time,
                end_time=end_time,
                title=title,
                description=description,
                investor_event_id=event["id"],
            )

            serializer = MeetingSerializer(meeting)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {investor_id} does not exist")
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {startup_id} does not exist")
        except CalendarError as e:
            raise InvestorError(str(e))
        except Exception as e:
            raise InvestorError(f"Error scheduling meeting: {str(e)}")
