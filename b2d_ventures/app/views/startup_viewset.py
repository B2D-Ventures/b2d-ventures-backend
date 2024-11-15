import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from b2d_ventures.app.models import Startup, Deal, Meeting, Investment
from b2d_ventures.app.serializers import (
    StartupSerializer,
    DealSerializer,
    MeetingSerializer,
    InvestmentSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from b2d_ventures.app.services import StartupService, StartupError
from b2d_ventures.utils import JSONParser, VndJsonParser, IsStartup
from b2d_ventures.utils.logger import CustomLogger

logger = CustomLogger().logger


class StartupViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Startup-related operations."""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    parser_classes = [JSONParser, VndJsonParser, MultiPartParser, FormParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStartup]

    @action(detail=True, methods=["get", "put"], url_path="profile")
    def profile(self, request, pk=None):
        """Get or update startup's profile."""
        logger.info(f"Fetching profile for startup ID: {pk}")
        try:
            if request.method == "GET":
                return StartupService.get_profile(pk)
            elif request.method == "PUT":
                attributes = request.data.get("data", {}).get("attributes", {})
                return StartupService.update_profile(pk, attributes)
        except ObjectDoesNotExist as e:
            logger.error(f"Profile not found for startup ID: {pk} - {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get", "post"], url_path="deals")
    def deals(self, request, pk=None):
        """List startup's deals or create a new deal."""
        logger.info(f"Listing or creating deals for startup ID: {pk}")
        try:
            if request.method == "GET":
                return StartupService.list_deals(pk)
            elif request.method == "POST":
                return self._create_deal(request, pk)
        except ObjectDoesNotExist as e:
            logger.error(f"Deals not found for startup ID: {pk} - {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
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
        methods=["put", "delete"],
        url_path="deals/(?P<deal_id>[^/.]+)",
    )
    def deal_operations(self, request, pk=None, deal_id=None):
        """Get, update or delete a specific deal."""
        logger.info(
            f"Performing deal operation for startup ID: {pk}, deal ID: {deal_id}"
        )
        try:
            service = StartupService()
            if request.method == "PUT":
                attributes = request.data
                return service.update_deal(pk, deal_id, attributes)
            elif request.method == "DELETE":
                return service.delete_deal(pk, deal_id)
        except ObjectDoesNotExist as e:
            logger.error(f"Deal not found for ID: {deal_id} - {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
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
        """List investments in the startup."""
        logger.info(f"Listing investments for startup ID: {pk}")
        try:
            return StartupService.list_investments(pk)
        except ObjectDoesNotExist as e:
            logger.error(f"Investments not found for startup ID: {pk} - {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="meetings")
    def list_meetings(self, request, pk=None):
        """List all meetings for the startup."""
        logger.info(f"Listing meetings for startup ID: {pk}")
        try:
            startup = Startup.objects.get(pk=pk)
            meetings = startup.meetings.all().order_by("start_time")
            serializer = MeetingSerializer(meetings, many=True)
            response_data = {
                "data": [
                    {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                    for meeting in serializer.data
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            logger.error(f"Startup with ID: {pk} does not exist")
            return Response(
                {"errors": [{"detail": f"Startup with id {pk} does not exist"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="dashboard")
    def dashboard(self, request, pk=None):
        """
        Get a comprehensive dashboard for the startup, including profile, deals, investments, meetings, and other relevant data.
        """
        logger.info(f"Fetching dashboard for startup ID: {pk}")
        try:
            startup = self.get_object()
            profile_response = self.profile(request, pk)
            deals_response = self.deals(request, pk)
            investments_response = self.list_investments(request, pk)
            meetings_response = self.list_meetings(request, pk)

            total_raised = startup.total_raised
            deal_count = Deal.objects.filter(startup=startup).count()
            active_deals = Deal.objects.filter(startup=startup, status="approved")
            active_deals_serializer = DealSerializer(active_deals, many=True)

            upcoming_meetings = Meeting.objects.filter(
                startup=startup, start_time__gt=timezone.now()
            ).order_by("start_time")[:5]
            upcoming_meetings_serializer = MeetingSerializer(
                upcoming_meetings, many=True
            )

            recent_investments = Investment.objects.filter(
                deal__startup=startup
            ).order_by("-investment_date")[:5]
            recent_investments_serializer = InvestmentSerializer(
                recent_investments, many=True
            )

            dashboard_data = {
                "type": "startup_dashboard",
                "id": str(startup.id),
                "attributes": {
                    "profile": profile_response.data.get("attributes", {}),
                    "deals": (
                        deals_response.data if hasattr(deals_response, "data") else []
                    ),
                    "investments": (
                        investments_response.data
                        if hasattr(investments_response, "data")
                        else []
                    ),
                    "meetings": meetings_response.data.get("data", []),
                    "total_raised": float(total_raised),
                    "deal_count": deal_count,
                    "fundraising_goal": float(startup.fundraising_goal),
                    "active_deals": [
                        {"type": "deal", "id": deal["id"], "attributes": deal}
                        for deal in active_deals_serializer.data
                    ],
                    "upcoming_meetings": [
                        {"type": "meeting", "id": meeting["id"], "attributes": meeting}
                        for meeting in upcoming_meetings_serializer.data
                    ],
                    "recent_investments": [
                        {
                            "type": "investment",
                            "id": investment["id"],
                            "attributes": investment,
                        }
                        for investment in recent_investments_serializer.data
                    ],
                },
            }

            return Response(dashboard_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            logger.error(f"Startup with ID: {pk} does not exist - {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logger.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def _create_deal(request, pk):
        logger.info(f"Creating deal for startup ID: {pk}")
        try:
            startup = Startup.objects.get(pk=pk)
            deal_data = request.data.copy()
            dataroom_file = request.FILES.get("dataroom")
            if dataroom_file:
                deal_data["dataroom"] = dataroom_file
            deal_data["startup_id"] = startup.id

            serializer = DealSerializer(data=deal_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(
                    f"Deal creation failed for startup ID: {pk} - {serializer.errors}"
                )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Startup.DoesNotExist:
            logger.error(f"Startup with ID: {pk} not found")
            return Response(
                {"errors": [{"detail": "Startup not found"}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error", "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
