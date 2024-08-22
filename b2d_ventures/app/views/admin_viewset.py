import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from b2d_ventures.app.serializers import (
    UserSerializer,
    DealSerializer,
    InvestmentSerializer,
    DataRoomSerializer,
    MeetingSerializer,
)
from b2d_ventures.app.services import AdminService, AdminError
from b2d_ventures.utils import JSONParser, VndJsonParser


class AdminViewSet(viewsets.ViewSet):
    """ViewSet for handling Admin-related operations."""

    parser_classes = [JSONParser, VndJsonParser]

    @action(detail=False, methods=['get'], url_path='users')
    def list_users(self, request):
        """List all users."""
        try:
            service = AdminService()
            users = service.list_users()
            serializer = UserSerializer(users, many=True)
            response_data = {
                "data": [
                    {"type": "users", "id": str(user.id),
                     "attributes": user_data}
                    for user, user_data in zip(users, serializer.data)
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=['get'], url_path='users')
    def get_user(self, request, pk=None):
        """Get a specific user."""
        try:
            service = AdminService()
            user = service.get_user_details(pk)
            serializer = UserSerializer(user)
            response_data = {
                "data": {"type": "users", "id": str(user.id),
                         "attributes": serializer.data}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "User not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['get'], url_path='deals')
    def list_deals(self, request):
        """List all deals."""
        try:
            service = AdminService()
            deals = service.list_deals()
            serializer = DealSerializer(deals, many=True)
            response_data = {
                "data": [
                    {"type": "deals", "id": str(deal.id),
                     "attributes": deal_data}
                    for deal, deal_data in zip(deals, serializer.data)
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=['put'],
            url_path='deals/(?P<deal_id>[^/.]+)/approve')
    def approve_deal(self, request, deal_id=None):
        """Approve a deal."""
        try:
            service = AdminService()
            deal = service.approve_deal(deal_id)
            serializer = DealSerializer(deal)
            response_data = {
                "data": {"type": "deals", "id": str(deal.id),
                         "attributes": serializer.data}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "Deal not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=['put'],
            url_path='deals/(?P<deal_id>[^/.]+)/reject')
    def reject_deal(self, request, deal_id=None):
        """Reject a deal."""
        try:
            service = AdminService()
            deal = service.reject_deal(deal_id)
            serializer = DealSerializer(deal)
            response_data = {
                "data": {"type": "deals", "id": str(deal.id),
                         "attributes": serializer.data}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "Deal not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['get'], url_path='investments')
    def list_investments(self, request):
        """List all investments."""
        try:
            service = AdminService()
            investments = service.list_investments()
            serializer = InvestmentSerializer(investments, many=True)
            response_data = {
                "data": [
                    {"type": "investments", "id": str(investment.id),
                     "attributes": investment_data}
                    for investment, investment_data in
                    zip(investments, serializer.data)
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['get'], url_path='datarooms')
    def list_datarooms(self, request):
        """List all data rooms."""
        try:
            service = AdminService()
            datarooms = service.list_datarooms()
            serializer = DataRoomSerializer(datarooms, many=True)
            response_data = {
                "data": [
                    {"type": "datarooms", "id": str(dataroom.id),
                     "attributes": dataroom_data}
                    for dataroom, dataroom_data in
                    zip(datarooms, serializer.data)
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['get'], url_path='meetings')
    def list_meetings(self, request):
        """List all meetings."""
        try:
            service = AdminService()
            meetings = service.list_meetings()
            serializer = MeetingSerializer(meetings, many=True)
            response_data = {
                "data": [
                    {"type": "meetings", "id": str(meeting.id),
                     "attributes": meeting_data}
                    for meeting, meeting_data in zip(meetings, serializer.data)
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['get'], url_path='dashboard')
    def get_dashboard(self, request):
        """Get admin dashboard data."""
        try:
            service = AdminService()
            dashboard_data = service.get_dashboard_data()
            response_data = {
                "data": {
                    "type": "dashboard",
                    "id": "admin_dashboard",
                    "attributes": dashboard_data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
