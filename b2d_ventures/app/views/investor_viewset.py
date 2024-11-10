import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from b2d_ventures.app.models import Investor, Deal, Meeting, Investment
from b2d_ventures.app.serializers import (
    InvestorSerializer,
    MeetingSerializer,
    DealSerializer,
)
from b2d_ventures.app.services import InvestorService, InvestorError
from b2d_ventures.utils import JSONParser, VndJsonParser



class InvestorViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Investor-related operations."""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    parser_classes = [JSONParser, VndJsonParser, MultiPartParser, FormParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="profile")
    def get_profile(self, request, pk=None):
        """Get investor's profile."""
        try:
            return InvestorService.get_profile(pk)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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

    @action(detail=True, methods=["get"], url_path="investments")
    def list_investments(self, request, pk=None):
        """List investments made by the investor."""
        try:
            return InvestorService.list_investments(pk)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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

    @action(detail=True, methods=["post"], url_path="investments/(?P<deal_id>[^/.]+)")
    def create_investment(self, request, pk=None, deal_id=None):
        """Create a new investment."""
        try:
            attributes = request.data.get("data", {}).get("attributes", {})
            return InvestorService.create_investment(pk, deal_id, attributes)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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

    @action(
        detail=True,
        methods=["post"],
        url_path="deals/(?P<deal_id>[^/.]+)/request-dataroom",
    )
    def request_dataroom(self, request, pk=None, deal_id=None):
        """Request access to a deal's dataroom."""
        try:
            return InvestorService.request_dataroom(pk, deal_id)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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

    @action(
        detail=True,
        methods=["post"],
        url_path="schedule-meeting/(?P<startup_id>[^/.]+)",
    )
    def schedule_meeting(self, request, pk=None, startup_id=None):
        """Schedule a meeting with a startup."""
        try:
            attributes = request.data.get("data", {}).get("attributes", {})
            return InvestorService.schedule_meeting(pk, startup_id, attributes)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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

    @action(detail=True, methods=["get"], url_path="meetings")
    def meetings(self, request, pk=None):
        """Get all meetings that belong to the investor."""
        try:
            investor = Investor.objects.get(pk=pk)
            meetings = investor.meetings.all().order_by("start_time")
            serializer = MeetingSerializer(meetings, many=True)
            response_data = [
                {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                for meeting in serializer.data
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            return Response(
                {"errors": [{"detail": f"Investor with id {pk} does not exist"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Error getting investor meetings: {e}")
            return Response(
                {
                    "errors": [
                        {
                            "detail": "Error getting investor meetings",
                            "meta": {"message": str(e)},
                        }
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="dashboard")
    def dashboard(self, request, pk=None):
        try:
            investor = self.get_object()
            profile_response = self.get_profile(request, pk)
            investments_response = self.list_investments(request, pk)
            meetings_response = self.meetings(request, pk)

            profile_data = profile_response.data.get("attributes", {})
            investments_data = investments_response.data
            meetings_data = meetings_response.data

            total_invested = (
                Investment.objects.filter(investor=investor).aggregate(
                    Sum("investment_amount")
                )["investment_amount__sum"]
                or 0
            )
            investment_count = Investment.objects.filter(investor=investor).count()
            active_deals = Deal.objects.filter(status="approved")
            active_deals_serializer = DealSerializer(active_deals, many=True)
            upcoming_meetings = Meeting.objects.filter(
                investor=investor, start_time__gt=timezone.now()
            ).order_by("start_time")[:5]
            upcoming_meetings_serializer = MeetingSerializer(
                upcoming_meetings, many=True
            )
            dashboard_data = {
                "type": "investor_dashboard",
                "id": str(investor.id),
                "attributes": {
                    "profile": profile_data,
                    "investments": investments_data,
                    "meetings": meetings_data,
                    "total_invested": float(total_invested),
                    "investment_count": investment_count,
                    "available_funds": float(investor.available_funds),
                    "active_deals": [
                        {"type": "deal", "id": deal["id"], "attributes": deal}
                        for deal in active_deals_serializer.data
                    ],
                    "upcoming_meetings": [
                        {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                        for meeting in upcoming_meetings_serializer.data
                    ],
                },
            }

            return Response(dashboard_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvestorError as e:
            logging.error(f"Investor error: {e}")
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
