"""The module defines the StartupService class and StartupError."""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from b2d_ventures.app.models import Startup, User, Deal, Investment, DataRoom
from b2d_ventures.app.serializers import (
    StartupSerializer,
    DealSerializer,
    InvestmentSerializer,
    DataRoomSerializer,
)


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
            response_data = {"type": "startups", "attributes": serializer.data}
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
            for key, value in attributes.items():
                setattr(startup_obj, key, value)
            startup_obj.save()
            serializer = StartupSerializer(startup_obj)
            response_data = {"type": "startups", "attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
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
            response_data = [
                {"type": "deals", "attributes": deal_data}
                for deal, deal_data in zip(deals, serializer.data)
            ]
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
            attributes["startup"] = startup
            deal = Deal.objects.create(**attributes)
            serializer = DealSerializer(deal)
            response_data = {"type": "deals", "attributes": serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
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
            response_data = {"type": "deals", "attributes": serializer.data}
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
            for key, value in attributes.items():
                setattr(deal, key, value)
            deal.save()
            serializer = DealSerializer(deal)
            response_data = {"type": "deals", "attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
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
                {"type": "investments", "attributes": investment_data}
                for investment, investment_data in zip(investments, serializer.data)
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error listing investments: {str(e)}")

    @staticmethod
    def get_dataroom(pk):
        """Get startup's data room."""
        try:
            startup = Startup.objects.get(id=pk)
            dataroom = DataRoom.objects.get(startup=startup)
            serializer = DataRoomSerializer(dataroom)
            response_data = {"type": "datarooms", "attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except DataRoom.DoesNotExist:
            raise ObjectDoesNotExist(f"Data room for startup {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error getting data room: {str(e)}")

    @staticmethod
    def update_dataroom(pk, attributes):
        """Update startup's data room."""
        try:
            startup = Startup.objects.get(id=pk)
            dataroom, created = DataRoom.objects.get_or_create(startup=startup)
            for key, value in attributes.items():
                setattr(dataroom, key, value)
            dataroom.save()
            serializer = DataRoomSerializer(dataroom)
            response_data = {"type": "datarooms", "attributes": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except Exception as e:
            raise StartupError(f"Error updating data room: {str(e)}")

    @staticmethod
    def manage_dataroom_access(pk, attributes):
        """Grant or revoke investor access to data room."""
        try:
            startup = Startup.objects.get(id=pk)
            dataroom = DataRoom.objects.get(startup=startup)
            investor = User.objects.get(id=attributes["investor_id"], role="investor")
            if attributes["grant_access"]:
                dataroom.access_permissions.add(investor)
            else:
                dataroom.access_permissions.remove(investor)
            response_data = {
                "type": "dataroom_access",
                "attributes": {
                    "success": True,
                    "message": "Data room access updated successfully",
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            raise ObjectDoesNotExist(f"Startup with id {pk} does not exist")
        except (DataRoom.DoesNotExist, User.DoesNotExist):
            raise ObjectDoesNotExist("Data room or investor not found")
        except Exception as e:
            raise StartupError(f"Error managing data room access: {str(e)}")
