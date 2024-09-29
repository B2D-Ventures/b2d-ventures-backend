import logging
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from google.oauth2.credentials import Credentials


from b2d_ventures.app.models import Investor
from b2d_ventures.app.serializers import InvestorSerializer
from b2d_ventures.app.services import InvestorService, InvestorError
from b2d_ventures.utils import JSONParser, VndJsonParser


class InvestorViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Investor-related operations."""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    parser_classes = [JSONParser, VndJsonParser, MultiPartParser, FormParser]

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
