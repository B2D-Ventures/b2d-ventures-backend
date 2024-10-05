from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from b2d_ventures.app.models import Admin, Investor, User
from b2d_ventures.app.services import AuthError

User = get_user_model()


class AuthViewSetTest(APITestCase):
    """
    Test suite for the AuthViewSet.

    This class contains tests for user authentication, creation, and role updates.
    """

    def setUp(self):
        """
        Set up test data for the AuthViewSet tests.
        """
        self.admin_user = Admin.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            role="admin",
        )
        self.client.force_authenticate(user=self.admin_user)

    @patch("b2d_ventures.app.services.AuthService.extract_authorization_code")
    @patch("b2d_ventures.app.services.AuthService.exchange_code_for_token")
    @patch("b2d_ventures.app.services.AuthService.get_user_profile")
    def test_create_new_user(
        self, mock_get_profile, mock_exchange_token, mock_extract_code
    ):
        """Test creating a new user via Google SSO."""
        mock_extract_code.return_value = "test_code"
        mock_exchange_token.return_value = {
            "access_token": "test_token",
            "refresh_token": "test_refresh",
        }
        mock_get_profile.return_value = {
            "email": "test@example.com",
            "name": "Test User",
        }

        url = "/api/auths/"
        data = {
            "data": {
                "attributes": {
                    "full_url": "http://example.com?code=test_code",
                    "role": "investor",
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["is_new_user"])
        self.assertEqual(Investor.objects.count(), 1)

    def test_create_user_missing_url(self):
        """Test creating a user with missing URL."""
        url = "/api/auths/"
        data = {"data": {"attributes": {"role": "investor"}}}
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_role(self):
        """Test creating a user with an invalid role."""
        url = "/api/auths/"
        data = {
            "data": {
                "attributes": {
                    "full_url": "http://example.com?code=test_code",
                    "role": "invalid_role",
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("b2d_ventures.app.services.AuthService.extract_authorization_code")
    def test_create_user_auth_error(self, mock_extract_code):
        """Test creating a user with AuthError."""
        mock_extract_code.side_effect = AuthError("Test error")

        url = "/api/auths/"
        data = {
            "data": {
                "attributes": {
                    "full_url": "http://example.com?code=test_code",
                    "role": "investor",
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_role_missing_role(self):
        """Test updating a user's role with missing role data."""
        url = "/api/auths/user_id/update-role/"
        data = {"data": {"attributes": {}}}
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_role_invalid_role(self):
        """Test updating a user's role with an invalid role."""
        url = "/api/auths/user_id/update-role/"
        data = {"data": {"attributes": {"role": "invalid_role"}}}
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("b2d_ventures.app.models.User.objects.filter")
    def test_update_role_user_not_found(self, mock_filter):
        """Test updating a role for a non-existent user."""
        mock_filter.return_value.first.return_value = None

        url = "/api/auths/user_id/update-role/"
        data = {"data": {"attributes": {"role": "investor"}}}
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_role_success(self):
        """Test successfully updating a user's role."""
        user = User.objects.create(
            email="test@example.com",
            username="Test User",
            refresh_token="test_token",
            role="unassigned",
        )

        url = f"/api/auths/{user.id}/update-role/"
        data = {"data": {"attributes": {"role": "investor"}}}
        response = self.client.put(url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["type"], "investor")

    @patch("b2d_ventures.app.models.User.objects.filter")
    def test_update_role_internal_error(self, mock_filter):
        """Test updating a role with an internal server error."""
        mock_filter.side_effect = Exception("Test error")

        url = "/api/auths/user_id/update-role/"
        data = {"data": {"attributes": {"role": "investor"}}}
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
