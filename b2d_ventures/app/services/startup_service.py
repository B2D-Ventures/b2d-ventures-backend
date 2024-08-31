"""The module defines the StartupService class and StartupError."""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from b2d_ventures.app.models import Startup, User, Deal, Investment
from b2d_ventures.app.serializers import (
    StartupSerializer,
    DealSerializer,
    InvestmentSerializer,
)
from icecream import ic


class StartupError(Exception):
    """Custom Exception for startup-related errors."""


class StartupService:
    """Class definition for StartupService."""

    @staticmethod
    def get_profile(pk):
        """Get startup's profile."""
        try:
            startup = Startup.objects.get(id=pk)
            serializer = StartupSerializer(startup)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error getting startup profile: {str(e)}")

    @staticmethod
    def update_profile(pk, attributes):
        """Update startup's profile."""
        try:
            startup_obj = Startup.objects.get(id=pk)
            serializer = StartupSerializer(startup_obj, data=attributes, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {"attributes": serializer.data}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error updating startup profile: {str(e)}")

    @staticmethod
    def list_deals(pk):
        """List startup's deals."""
        try:
            startup = Startup.objects.get(id=pk)
            deals = Deal.objects.filter(startup=startup)
            serializer = DealSerializer(deals, many=True)
            response_data = [{"attributes": deal_data} for deal_data in serializer.data]
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error listing startup deals: {str(e)}")

    @staticmethod
    def create_deal(pk, attributes):
        """Create a new deal."""
        try:
            startup = Startup.objects.get(id=pk)
            attributes["startup"] = startup.id
            serializer = DealSerializer(data=attributes)
            if serializer.is_valid():
                serializer.save()
                response_data = {"attributes": serializer.data}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error creating deal: {str(e)}")

    @staticmethod
    def get_deal_details(pk, deal_id):
        """Get details of a specific deal."""
        try:
            startup = Startup.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id, startup=startup)
            serializer = DealSerializer(deal)
            response_data = {"attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Deal with id {deal_id} does not exist for this startup"
            )
        except Exception as e:
            raise StartupError(f"Error getting deal details: {str(e)}")

    @staticmethod
    def update_deal(pk, deal_id, attributes):
        """Update a specific deal."""
        try:
            startup = Startup.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id, startup=startup)
            serializer = DealSerializer(deal, data=attributes, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {"attributes": serializer.data}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Deal with id {deal_id} does not exist for this startup"
            )
        except Exception as e:
            raise StartupError(f"Error updating deal: {str(e)}")

    @staticmethod
    def delete_deal(pk, deal_id):
        """Delete a specific deal."""
        ic("deleting")
        try:
            startup = Startup.objects.get(id=pk)
            deal = Deal.objects.get(id=deal_id, startup=startup)
            deal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Deal with id {deal_id} does not exist for this startup"
            )
        except Exception as e:
            raise StartupError(f"Error deleting deal: {str(e)}")

    @staticmethod
    def list_investments(pk):
        """List investments in the startup."""
        try:
            startup = Startup.objects.get(id=pk)
            investments = Investment.objects.filter(deal__startup=startup)
            serializer = InvestmentSerializer(investments, many=True)
            response_data = [
                {"attributes": investment_data} for investment_data in serializer.data
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error listing investments: {str(e)}")

    # @staticmethod
    # def request_dataroom_access(pk, attributes):
    #     """Grant or revoke investor access to data room."""
    #     try:
    #         startup = Startup.objects.get(id=pk)
    #         dataroom = DataRoom.objects.get(startup=startup)
    #         investor = User.objects.get(id=attributes["investor_id"],
    #                                     role="investor")
    #
    #         current_permissions = dataroom.access_permissions.split(
    #             ',') if dataroom.access_permissions else []
    #
    #         if attributes["grant_access"]:
    #             if str(investor.id) not in current_permissions:
    #                 current_permissions.append(str(investor.id))
    #         else:
    #             if str(investor.id) in current_permissions:
    #                 current_permissions.remove(str(investor.id))
    #
    #         dataroom.access_permissions = ','.join(current_permissions)
    #         dataroom.save()
    #
    #         response_data = {
    #             "attributes": {
    #                 "success": True,
    #                 "message": "Data room access updated successfully",
    #             },
    #         }
    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Startup.DoesNotExist:
    #         raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
    #     except (DataRoom.DoesNotExist, User.DoesNotExist):
    #         raise ObjectDoesNotExist("Data room or investor not found")
    #     except Exception as e:
    #         raise StartupError(f"Error managing data room access: {str(e)}")
