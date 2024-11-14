"""A module that defines the AuthViewSet class."""

import logging
from typing import Dict, Any, Union, Tuple

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthViewSet(viewsets.ViewSet):
    """ViewSet for handling User authentication and creation."""

    parser_classes = [JSONParser, VndJsonParser]
    authentication_classes = [JWTAuthentication]

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

        if role not in ["admin", "investor", "startup", "unassigned"]:
            return Response(
                {"errors": [{"detail": "Invalid role provided"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            authorization_code = self.auth_service.extract_authorization_code(full_url)
            if not authorization_code:
                raise AuthError("Authorization code not found in URL")
            tokens = self.auth_service.exchange_code_for_token(authorization_code)
            refresh_token = tokens.get("refresh_token", "")
            user_profile = self.auth_service.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")
            user, created, actual_role = self._create_or_update_user(
                role, user_email, user_profile, refresh_token, not_update=True
            )
            serializer = self._get_serializer_for_role(actual_role, user)
            jwt_tokens = self._generate_jwt_tokens(user)

            response_data = {
                "attributes": serializer.data,
                "is_new_user": created,
                "jwt_tokens": jwt_tokens,
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

    @action(
        detail=True,
        methods=["put"],
        url_path="update-role",
    )
    def update_role(self, request, pk=None):
        """
        Update a user's role by deleting the existing User and creating a new role-specific user.
        """
        attributes = request.data.get("data", {}).get("attributes", {})
        new_role = attributes.get("role")

        if not new_role:
            return Response(
                {"errors": [{"detail": "New role is required"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_role not in [
            "investor",
            "startup",
            "pending_investor",
            "pending_startup",
            "unassigned",
        ]:
            return Response(
                {"errors": [{"detail": "Invalid role provided"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                existing_user = User.objects.filter(id=pk).first()

                if not existing_user:
                    return Response(
                        {"errors": [{"detail": "User not found"}]},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                email = existing_user.email
                user_profile = {
                    "name": existing_user.username,
                }
                refresh_token = existing_user.refresh_token

                existing_user.delete()
                new_user, created, actual_role = self._create_or_update_user(
                    new_role, email, user_profile, refresh_token
                )

                serializer = self._get_serializer_for_role(new_role, new_user)
                return Response(
                    {
                        "type": actual_role,
                        "id": new_user.id,
                        "attributes": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            logging.error(f"Error updating user role: {e}")
            return Response(
                {
                    "errors": [
                        {
                            "detail": "Error updating user role",
                            "meta": {"message": str(e)},
                        }
                    ]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], url_path="refresh-token")
    def refresh_token(self, request: Request) -> Response:
        """Endpoint to refresh JWT access token."""
        refresh_token = (
            request.data.get("data", {}).get("attributes", {}).get("refresh-token")
        )
        if not refresh_token:
            return Response(
                {"errors": [{"detail": "Refresh token is required"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Token refresh error: {e}")
            return Response(
                {"errors": [{"detail": "Token refresh failed"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _create_or_update_user(
        self,
        role: str,
        user_email: str,
        user_profile: Dict[str, Any],
        refresh_token: str,
        not_update: bool = False,
    ) -> Tuple[Union[Admin, Investor, Startup, User], bool, str]:
        """Create or update a user based on their role."""
        existing_user, existing_role = self._check_existing_user(user_email, role)

        if existing_user:
            if existing_role != role and not not_update:
                existing_user.role = role
                existing_user.save()
            return existing_user, False, existing_role

        if role == "admin":
            user = Admin.objects.create(
                email=user_email,
                username=user_profile.get("name"),
                refresh_token=refresh_token,
            )
        elif role == "investor":
            user = Investor.objects.create(
                email=user_email,
                username=user_profile.get("name"),
                refresh_token=refresh_token,
            )
        elif role == "startup":
            user = Startup.objects.create(
                email=user_email,
                username=user_profile.get("name"),
                name=user_profile.get("name"),
                refresh_token=refresh_token,
            )
        else:
            user = User.objects.create(
                email=user_email,
                username=user_profile.get("name"),
                refresh_token=refresh_token,
                role=role,
            )

        return user, True, role

    def _check_existing_user(
        self, user_email: str, role: str = "Unassigned"
    ) -> Tuple[Union[Admin, Investor, Startup, User, None], str]:
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

        try:
            user = User.objects.get(email=user_email)
            return user, user.role
        except User.DoesNotExist:
            pass

        return None, role

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

    def _generate_jwt_tokens(self, user: User) -> Dict[str, str]:
        """Generate access and refresh tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            "jwt_refresh_token": str(refresh),
            "jwt_access_token": str(refresh.access_token),
        }
