"""A module that defines the AuthViewSet class."""

import logging
from typing import Dict, Any, Union, Tuple

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from b2d_ventures.app.models import Admin, Investor, Startup, User
from b2d_ventures.app.serializers import (
    AdminSerializer,
    InvestorSerializer,
    StartupSerializer,
    UserSerializer,
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

        if not full_url:
            return Response(
                {"errors": [{"detail": "Full URL is required"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role not in ["admin", "investor", "startup", "null"]:
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

            user, created, actual_role = self._create_or_update_user(role, user_email, user_profile)

            serializer = self._get_serializer_for_role(actual_role, user)

            response_data = {
                "type": actual_role,
                "attributes": serializer.data,
                "is_new_user": created,
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

    def _check_existing_user(self, user_email: str) -> Tuple[Union[Admin, Investor, Startup, None], str]:
        """Check if a user exists and return their instance and role."""
        try:
            admin = Admin.objects.get(email=user_email)
            return admin, "admin"
        except Admin.DoesNotExist:
            pass

        try:
            investor = Investor.objects.get(email=user_email)
            return investor, "investor"
        except Investor.DoesNotExist:
            pass

        try:
            startup = Startup.objects.get(email=user_email)
            return startup, "startup"
        except Startup.DoesNotExist:
            pass

        return None, "null"

    def _create_or_update_user(
        self, role: str, user_email: str, user_profile: Dict[str, Any]
    ) -> Tuple[Union[Admin, Investor, Startup, User], bool, str]:
        """Create or update a user based on their role."""
        existing_user, existing_role = self._check_existing_user(user_email)

        if existing_user and role == "null":
            return existing_user, False, existing_role

        if role == "null":
            user, created = User.objects.get_or_create(
                email=user_email,
                defaults={
                    "username": user_profile.get("name"),
                }
            )
            return user, created, "null"

        if role == "admin":
            user, created = Admin.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "permission": "full",
                },
            )
        elif role == "investor":
            user, created = Investor.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "available_funds": 0,
                    "total_invested": 0,
                },
            )
        elif role == "startup":
            user, created = Startup.objects.update_or_create(
                email=user_email,
                defaults={
                    "email": user_email,
                    "username": user_profile.get("name"),
                    "name": user_profile.get("name"),
                    "description": "",
                },
            )
        else:
            raise AuthError("Invalid role provided")

        return user, created, role

    def _get_serializer_for_role(
        self, role: str, user: Union[Admin, Investor, Startup, User]
    ) -> Union[AdminSerializer, InvestorSerializer, StartupSerializer, UserSerializer]:
        """Get the appropriate serializer based on the user's role."""
        if role == "admin":
            return AdminSerializer(user)
        elif role == "investor":
            return InvestorSerializer(user)
        elif role == "startup":
            return StartupSerializer(user)
        else:
            return UserSerializer(user)