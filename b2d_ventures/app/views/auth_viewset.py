"""A module that defines the AuthViewSet class."""

import logging

from django.core.exceptions import ObjectDoesNotExist
from icecream import ic
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from b2d_ventures.app.models import User, Admin, Investor, Startup
from b2d_ventures.app.serializers import (
    UserSerializer,
    AdminSerializer,
    InvestorSerializer,
    StartupSerializer,
)
from b2d_ventures.app.services import AuthService, AuthError
from b2d_ventures.utils import JSONParser, VndJsonParser


class AuthViewSet(viewsets.ModelViewSet):
    """ModelViewSet for handling User-related operations."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [JSONParser, VndJsonParser]

    def create(self, request, *args, **kwargs):
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
            service = AuthService()
            authorization_code = service.extract_authorization_code(full_url)
            if not authorization_code:
                raise AuthError("Authorization code not found in URL")

            tokens = service.exchange_code_for_token(authorization_code)
            user_profile = service.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")
            ic(user_profile)

            if role == "admin":
                user, created = Admin.objects.update_or_create(
                    email=user_email,
                    defaults={
                        "email": user_email,
                        "username": user_profile.get("name"),
                        "permission": "full",
                    },
                )
                serializer = AdminSerializer(user)
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
                serializer = InvestorSerializer(user)
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
                serializer = StartupSerializer(user)

            response_data = {
                "type": role,
                "id": str(user.id),
                "attributes": serializer.data,
            }

            return Response(
                response_data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except AuthError as e:
            logging.error(f"Authorization error: {e}")
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
