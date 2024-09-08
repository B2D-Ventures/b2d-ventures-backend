"""The module defines the InvestorService class and InvestorError."""
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from b2d_ventures.app.models import Investor, Deal, Investment
from b2d_ventures.app.serializers import (
    InvestorSerializer,
    InvestmentSerializer,
)
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
        """Request access to a deal's dataroom and send it via email."""
        try:
            investor = Investor.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id)

            if not deal.dataroom:
                raise InvestorError(
                    "No dataroom file available for this deal.")

            investor_email = investor.email
            dataroom_file = deal.dataroom

            email_service = EmailService()
            email_subject = f"Dataroom Access for {deal.name}"
            email_body = f"Dear {investor.username},\n\nPlease find attached the dataroom for the deal: {deal.name}."

            email_service.send_email_with_attachment(
                to_email=investor_email,
                subject=email_subject,
                body=email_body,
                attachment=dataroom_file,
                filename=f"{deal.name}_dataroom.pdf"
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
