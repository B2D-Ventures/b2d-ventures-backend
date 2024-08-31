import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from b2d_ventures.app.models import Startup
from b2d_ventures.app.serializers import StartupSerializer
from b2d_ventures.app.services import StartupService, StartupError
from b2d_ventures.utils import JSONParser, VndJsonParser


class StartupViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Startup-related operations."""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    parser_classes = [JSONParser, VndJsonParser]

    @action(detail=True, methods=["get", "put"], url_path="profile")
    def profile(self, request, pk=None):
        """Get or update startup's profile."""
        try:
            if request.method == "GET":
                return StartupService.get_profile(pk)
            elif request.method == "PUT":
                attributes = request.data.get("data", {}).get("attributes", {})
                return StartupService.update_profile(pk, attributes)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logging.error(f"Startup error: {e}")
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

    @action(detail=True, methods=["get", "post"], url_path="deals")
    def deals(self, request, pk=None):
        """List startup's deals or create a new deal."""
        try:
            if request.method == "GET":
                return StartupService.list_deals(pk)
            elif request.method == "POST":
                attributes = request.data.get("data", {}).get("attributes", {})
                return StartupService.create_deal(pk, attributes)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logging.error(f"Startup error: {e}")
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
        methods=["get", "put", "delete"],
        url_path="deals/(?P<deal_id>[^/.]+)",
    )
    def deal_details(self, request, pk=None, deal_id=None):
        """Get, update or delete a specific deal."""
        try:
            if request.method == "GET":
                return StartupService.get_deal_details(pk, deal_id)
            elif request.method == "PUT":
                attributes = request.data.get("data", {}).get("attributes", {})
                return StartupService.update_deal(pk, deal_id, attributes)
            elif request.method == "DELETE":
                return StartupService.delete_deal(pk, deal_id)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logging.error(f"Startup error: {e}")
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
        """List investments in the startup."""
        try:
            return StartupService.list_investments(pk)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logging.error(f"Startup error: {e}")
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

    @action(detail=True, methods=["get", "post", "put"], url_path="dataroom")
    def dataroom(self, request, pk=None):
        """Get, create or update startup's data room."""
        try:
            if request.method == "GET":
                return StartupService.get_dataroom(pk)
            elif request.method == "POST":
                return StartupService.create_dataroom(pk, request)
            elif request.method == "PUT":
                return StartupService.update_dataroom(pk, request)
        except ObjectDoesNotExist as e:
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StartupError as e:
            logging.error(f"Startup error: {e}")
            return Response(
                {"errors": [{"detail": str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {
                    "errors": [
                        {"detail": "Internal Server Error",
                         "meta": {"message": str(e)}}
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
