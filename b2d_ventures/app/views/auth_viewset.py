"""A module that defines the AuthViewSet class."""

import logging
from typing import Dict, Any, Union

from icecream import ic
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from b2d_ventures.app.models import Admin, Investor, Startup
from b2d_ventures.app.serializers import (
    AdminSerializer,
    InvestorSerializer,
    StartupSerializer,
)
from b2d_ventures.app.services import AuthService, AuthError
from b2d_ventures.utils import JSONParser, VndJsonParser


class AuthViewSet(viewsets.ViewSet):
    """ViewSet for handling User authentication and creation."""

    parser_classes = [JSONParser, VndJsonParser]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create or authenticate a user via Google SSO.

        :param request: The incoming HTTP request with the full Google auth URL and role.
        :return: HTTP Response with user data and token or an error message.
        """
        request_data = request.data.get("data", {})
        attributes = request_data.get("attributes", {})
        full_url = attributes.get("full_url")
        role = attributes.get("role")

        if not full_url or not role:
            return Response(
                {"errors": [{"detail": "Full URL and role are required"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role not in ["admin", "investor", "startup"]:
            return Response(
                {"errors": [{"detail": "Invalid role provided"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            authorization_code = self.auth_service.extract_authorization_code(full_url)
            if not authorization_code:
                raise AuthError("Authorization code not found in URL")

            tokens = self.auth_service.exchange_code_for_token(authorization_code)
            user_profile = self.auth_service.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")
            ic(user_profile)

            user, created = self._create_or_update_user(role, user_email, user_profile)
            serializer = self._get_serializer_for_role(role, user)

            response_data = {
                "type": role,
                "attributes": serializer.data,
            }

            return Response(
                response_data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except AuthError as e:
            logging.error(f"Authorization error: {e}")
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

    def _create_or_update_user(
        self, role: str, user_email: str, user_profile: Dict[str, Any]
    ) -> Union[Admin, Investor, Startup]:
        """Create or update a user based on their role."""
        if role == "admin":
            return Admin.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "permission": "full",
                },
            )
        elif role == "investor":
            return Investor.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "available_funds": 0,
                    "total_invested": 0,
                },
            )
        elif role == "startup":
            return Startup.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "name": user_profile.get("name"),
                    "description": "",
                },
            )

    def _get_serializer_for_role(
        self, role: str, user: Union[Admin, Investor, Startup]
    ) -> Union[AdminSerializer, InvestorSerializer, StartupSerializer]:
        """Get the appropriate serializer based on the user's role."""
        if role == "admin":
            return AdminSerializer(user)
        elif role == "investor":
            return InvestorSerializer(user)
        elif role == "startup":
            return StartupSerializer(user)
