"""The module defines the InvestorService class and InvestorError."""
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from b2d_ventures.app.models import Investor, Deal, Investment, Meeting
from b2d_ventures.app.serializers import (
    InvestorSerializer,
    InvestmentSerializer,
    MeetingSerializer,
)


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
                {"attributes": investment_data} for investment_data in
                serializer.data
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
            investment_amount = attributes.get("investment_amount")

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

            deal.raised += net_investment
            deal.investor_count += 1
            deal.save()

            investment = Investment.objects.create(
                deal=deal, investor=investor,
                investment_amount=investment_amount
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
            investment = Investment.objects.get(id=investment_id,
                                                investor=investor)
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
        """Request access to a deal's dataroom."""
        try:
            investor = Investor.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id)
            # Here you would implement the logic for requesting dataroom access
            # This might involve creating a new model for dataroom access requests
            # For now, we'll just return a success message
            return Response(
                {"message": "Dataroom access requested successfully"},
                status=status.HTTP_200_OK,
            )
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except Exception as e:
            raise InvestorError(f"Error requesting dataroom access: {str(e)}")

    @staticmethod
    def list_meetings(pk):
        """List meetings for the investor."""
        try:
            investor = Investor.objects.get(id=pk)
            meetings = Meeting.objects.filter(investor=investor)
            serializer = MeetingSerializer(meetings, many=True)
            response_data = [
                {"attributes": meeting_data} for meeting_data in
                serializer.data
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Exception as e:
            raise InvestorError(f"Error listing meetings: {str(e)}")

    @staticmethod
    def request_meeting(pk, attributes):
        """Request a new meeting."""
        try:
            investor = Investor.objects.get(id=pk)
            attributes["investor"] = investor.id
            serializer = MeetingSerializer(data=attributes)
            if serializer.is_valid():
                serializer.save()
                response_data = {"attributes": serializer.data}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Exception as e:
            raise InvestorError(f"Error requesting meeting: {str(e)}")

    @staticmethod
    def get_meeting(pk, meeting_id):
        """Get details of a specific meeting."""
        try:
            investor = Investor.objects.get(id=pk)
            meeting = Meeting.objects.get(id=meeting_id, investor=investor)
            serializer = MeetingSerializer(meeting)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Meeting.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Meeting with id {meeting_id} does not exist for this investor"
            )
        except Exception as e:
            raise InvestorError(f"Error getting meeting details: {str(e)}")

    @staticmethod
    @transaction.atomic
    def schedule_meeting(pk, deal_id, date, start_time, end_time, note):
        """Schedule a meeting with a startup."""
        try:
            investor = Investor.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id)
            startup = deal.startup

            # Combine date and time
            start_datetime = datetime.combine(
                datetime.strptime(date, "%Y-%m-%d").date(),
                datetime.strptime(start_time, "%H:%M").time()
            )
            end_datetime = datetime.combine(
                datetime.strptime(date, "%Y-%m-%d").date(),
                datetime.strptime(end_time, "%H:%M").time()
            )

            # Check if the meeting time is in the future
            if start_datetime <= timezone.now():
                raise InvestorError("Meeting time must be in the future")

            # Check if there's an active deal between the investor and the startup
            if not Deal.objects.filter(
                    id=deal_id,
                    startup=startup,
                    status="approved"
            ).exists():
                raise InvestorError(
                    "No active deal found between the investor and the startup")

            # Check for conflicting meetings
            if Meeting.objects.filter(
                    investor=investor,
                    date__range=(start_datetime, end_datetime)
            ).exists() or Meeting.objects.filter(
                startup=startup,
                date__range=(start_datetime, end_datetime)
            ).exists():
                raise InvestorError(
                    "The proposed time slot conflicts with an existing meeting")

            # Create the meeting
            # TODO: มาแก้ตาม meeting model ด้วย จะไปเล่นเกม สู้ๆ
            meeting = Meeting.objects.create(
                investor=investor,
                startup=startup,
                deal=deal,
                date=start_datetime,
                end_time=end_datetime,
                status="pending",
                note=note
            )

            # Here you would typically send notifications to both parties
            # For now, we'll just print a message
            print(
                f"Meeting scheduled: Investor {investor.id} with Startup {startup.id}")

            serializer = MeetingSerializer(meeting)
            return {
                "status": "success",
                "message": "Meeting scheduled successfully",
                "meeting": serializer.data
            }

        except Investor.DoesNotExist:
            raise ObjectDoesNotExist(f"Investor with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except InvestorError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            raise InvestorError(f"Error scheduling meeting: {str(e)}")