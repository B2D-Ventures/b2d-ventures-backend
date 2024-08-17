"""A module that defines the UserViewSet class."""
import logging

from b2d_ventures.app.services import UserService, UserError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from b2d_ventures.app.models import User, Admin, Investor, Startup
from b2d_ventures.app.serializers import UserSerializer, AdminSerializer, \
    InvestorSerializer, StartupSerializer


class UserViewSet(viewsets.ViewSet):
    """ViewSet for handling User-related operations."""

    def list(self, request):
        """
        List all User objects.

        :param request: The incoming HTTP request.
        :return: HTTP Response with list of user data.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create or authenticate a user via Google SSO.

        :param request: The incoming HTTP request with the full Google auth URL and role.
        :return: HTTP Response with user data and token or an error message.
        """
        full_url = request.data.get("full_url")
        role = request.data.get("role")
        logging.info(f"Full URL: {full_url}")
        logging.info(f"Role: {role}")

        if not full_url or not role:
            return Response(
                {"error": "Full URL and role are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role not in ['admin', 'investor', 'startup']:
            return Response(
                {"error": "Invalid role provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service = UserService()
            authorization_code = service.extract_authorization_code(full_url)
            if not authorization_code:
                raise UserError("Authorization code not found in URL")

            tokens = service.exchange_code_for_token(authorization_code)
            user_profile = service.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")
            logging.info(f"User email: {user_email}")

            # Create or update user based on role
            if role == 'admin':
                user, created = Admin.objects.update_or_create(
                    email=user_email,
                    defaults={
                        "email": user_email,
                        "username": user_profile.get("name"),
                        "role": role,
                        "permission": "full"
                    }
                )
                serializer = AdminSerializer(user)
            elif role == 'investor':
                user, created = Investor.objects.update_or_create(
                    email=user_email,
                    defaults={
                        "email": user_email,
                        "username": user_profile.get("name"),
                        "role": role,
                        "available_funds": 0,
                        "total_invested": 0
                    }
                )
                serializer = InvestorSerializer(user)
            elif role == 'startup':
                user, created = Startup.objects.update_or_create(
                    email=user_email,
                    defaults={
                        "email": user_email,
                        "username": user_profile.get("name"),
                        "role": role,
                        "name": user_profile.get("name"),
                        "description": ""
                    }
                )
                serializer = StartupSerializer(user)

            return Response(
                {
                    "user": serializer.data,
                    "token": tokens["access_token"],
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except AuthorizationError as e:
            logging.error(f"Authorization error: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """
        Retrieve a User object by ID.

        :param request: The incoming HTTP request.
        :param pk: The primary key of the user to be retrieved.
        :return: HTTP Response with user data or an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Update an existing User object by ID.

        :param request: The incoming HTTP request with updated User data.
        :param pk: The primary key of the user to be updated.
        :return: HTTP Response with updated user data or an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a User object by ID.

        :param request: The incoming HTTP request.
        :param pk: The primary key of the user to be deleted.
        :return: HTTP Response indicating successful deletion or an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def get_user_type(self, request, pk=None):
        """
        Get the type of a user.

        :param request: The incoming HTTP request.
        :param pk: The primary key of the user.
        :return: HTTP Response with the user type.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if isinstance(user, Admin):
            return Response({"type": "Admin"})
        elif isinstance(user, Investor):
            return Response({"type": "Investor"})
        elif isinstance(user, Startup):
            return Response({"type": "Startup"})
        else:
            return Response({"type": "User"})
