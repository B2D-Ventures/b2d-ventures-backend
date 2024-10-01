import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from b2d_ventures.app.models import User, Deal, Investment, Meeting, Admin
from b2d_ventures.app.serializers import (
    UserSerializer,
    DealSerializer,
    InvestmentSerializer,
    MeetingSerializer,
)
from b2d_ventures.app.services import AdminService, AdminError
from b2d_ventures.utils import JSONParser, VndJsonParser


class AdminViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Admin-related operations."""

    queryset = Admin.objects.all()
    serializer_class = UserSerializer
    parser_classes = [JSONParser, VndJsonParser]

    @action(detail=False, methods=["get"], url_path="users")
    def list_users(self, request):
        """List all users with their roles."""
        try:
            service = AdminService()
            users = service.list_users()
            serializer = UserSerializer(users, many=True)
            response_data = [
                {
                    "attributes": user_data,
                }
                for user, user_data in zip(users, serializer.data)
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["delete"], url_path="users")
    def delete_user(self, request, pk=None):
        """Get, update or delete a specific user."""
        try:
            service = AdminService()
            if request.method == "GET":
                user = service.get_user_details(pk)
                serializer = UserSerializer(user)
                response_data = {
                    "attributes": serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            elif request.method == "DELETE":
                service.delete_user(pk)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "User not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="deals")
    def list_deals(self, request):
        """List all deals."""
        try:
            service = AdminService()
            deals = service.list_deals()
            serializer = DealSerializer(deals, many=True)
            response_data = [
                {"attributes": deal_data}
                for deal, deal_data in zip(deals, serializer.data)
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["put", "delete"], url_path="deals")
    def deal_operations(self, request, pk=None):
        """Approve, reject or delete a deal."""
        try:
            service = AdminService()
            if request.method == "PUT":
                action = (
                    request.data.get("data", {}).get("attributes", {}).get("action")
                )
                if action == "approve":
                    deal = service.approve_deal(pk)
                elif action == "reject":
                    deal = service.reject_deal(pk)
                else:
                    return Response(
                        {"errors": [{"detail": "Invalid action"}]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                serializer = DealSerializer(deal)
                response_data = {"attributes": serializer.data}
                return Response(response_data, status=status.HTTP_200_OK)
            elif request.method == "DELETE":
                service.delete_deal(pk)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "Deal not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="investments")
    def list_investments(self, request):
        """List all investments."""
        try:
            service = AdminService()
            investments = service.list_investments()
            serializer = InvestmentSerializer(investments, many=True)
            response_data = [
                {"attributes": investment_data}
                for investment, investment_data in zip(investments, serializer.data)
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["delete"], url_path="investments")
    def delete_investment(self, request, pk=None):
        """Delete an investment."""
        try:
            service = AdminService()
            service.delete_investment(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"errors": [{"detail": "Investment not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="meetings")
    def list_meetings(self, request):
        """List all meetings."""
        try:
            service = AdminService()
            meetings = service.list_meetings()
            serializer = MeetingSerializer(meetings, many=True)
            response_data = {
                "data": [
                    {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                    for meeting in serializer.data
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"errors": [{"detail": "Internal Server Error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request):
        """
        Get a comprehensive dashboard for the admin, including user statistics, deals, investments, meetings, and other relevant data.
        """
        try:
            service = AdminService()
            dashboard_data = service.get_dashboard_data()

            recent_users = User.objects.order_by("-date_joined")[:5]
            recent_deals = Deal.objects.order_by("-start_date")[:5]
            recent_investments = Investment.objects.order_by("-investment_date")[:5]
            upcoming_meetings = Meeting.objects.filter(
                start_time__gt=timezone.now()
            ).order_by("start_time")[:5]

            recent_users_serializer = UserSerializer(recent_users, many=True)
            recent_deals_serializer = DealSerializer(recent_deals, many=True)
            recent_investments_serializer = InvestmentSerializer(
                recent_investments, many=True
            )
            upcoming_meetings_serializer = MeetingSerializer(
                upcoming_meetings, many=True
            )

            response_data = {
                "type": "admin_dashboard",
                "attributes": {
                    "statistics": dashboard_data,
                    "recent_users": [
                        {"type": "user", "id": user["id"], "attributes": user}
                        for user in recent_users_serializer.data
                    ],
                    "recent_deals": [
                        {"type": "deal", "id": deal["id"], "attributes": deal}
                        for deal in recent_deals_serializer.data
                    ],
                    "recent_investments": [
                        {
                            "type": "investment",
                            "id": investment["id"],
                            "attributes": investment,
                        }
                        for investment in recent_investments_serializer.data
                    ],
                    "upcoming_meetings": [
                        {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                        for meeting in upcoming_meetings_serializer.data
                    ],
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except AdminError as e:
            logging.error(f"Admin error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
