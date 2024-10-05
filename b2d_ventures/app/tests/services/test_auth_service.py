"""Test module for the AuthService class."""

from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from b2d_ventures.app.services.auth_service import AuthService, AuthError


class AuthServiceTestCase(TestCase):
    """
    Test case for the AuthService class.

    This class contains unit tests for all methods in the AuthService class,
    including error cases and edge scenarios.
    """

    def setUp(self):
        """Set up the test environment."""
        self.auth_service = AuthService()

    def test_extract_authorization_code(self):
        """
        Test the extract_authorization_code method.

        Verifies that the method correctly extracts the authorization code from a URL.
        """
        url = "http://example.com/callback?code=test_code&state=test_state"
        code = self.auth_service.extract_authorization_code(url)
        self.assertEqual(code, "test_code")

    def test_extract_authorization_code_missing(self):
        """
        Test the extract_authorization_code method with a missing code.

        Verifies that the method returns None when the code is not present in the URL.
        """
        url = "http://example.com/callback?state=test_state"
        code = self.auth_service.extract_authorization_code(url)
        self.assertIsNone(code)

    @patch("b2d_ventures.utils.HTTPRequestHandler.make_request")
    def test_exchange_code_for_token(self, mock_make_request):
        """
        Test the exchange_code_for_token method.

        Verifies that the method correctly exchanges an authorization code for a token.
        """
        mock_make_request.return_value = {"access_token": "test_token"}
        result = self.auth_service.exchange_code_for_token("test_code")
        self.assertEqual(result, {"access_token": "test_token"})
        mock_make_request.assert_called_once()

    @patch("b2d_ventures.utils.HTTPRequestHandler.make_request")
    def test_get_user_profile(self, mock_make_request):
        """
        Test the get_user_profile method.

        Verifies that the method correctly retrieves a user profile using an access token.
        """
        mock_make_request.return_value = {
            "name": "Test User",
            "email": "test@example.com",
        }
        result = self.auth_service.get_user_profile("test_token")
        self.assertEqual(result, {"name": "Test User", "email": "test@example.com"})
        mock_make_request.assert_called_once()

    @patch("b2d_ventures.utils.HTTPRequestHandler.make_request")
    def test_refresh_access_token_success(self, mock_make_request):
        """
        Test the refresh_access_token method for a successful case.

        Verifies that the method correctly refreshes an access token using a refresh token.
        """
        mock_make_request.return_value = {"access_token": "new_test_token"}
        result = self.auth_service.refresh_access_token("test_refresh_token")
        self.assertEqual(result, "new_test_token")
        mock_make_request.assert_called_once()

    @patch("b2d_ventures.utils.HTTPRequestHandler.make_request")
    def test_refresh_access_token_failure(self, mock_make_request):
        """
        Test the refresh_access_token method for a failure case.

        Verifies that the method raises an AuthError when the token refresh fails.
        """
        mock_make_request.return_value = {"error": "invalid_grant"}
        with self.assertRaises(AuthError):
            self.auth_service.refresh_access_token("test_refresh_token")

    @patch("b2d_ventures.utils.HTTPRequestHandler.make_request")
    def test_refresh_access_token_exception(self, mock_make_request):
        """
        Test the refresh_access_token method when an exception occurs.

        Verifies that the method raises an AuthError when an exception occurs during the refresh process.
        """
        mock_make_request.side_effect = Exception("Network error")
        with self.assertRaises(AuthError):
            self.auth_service.refresh_access_token("test_refresh_token")

    def test_settings_configuration(self):
        """
        Test the settings configuration.

        Verifies that the required settings are properly configured.
        """
        self.assertTrue(hasattr(settings, "TOKEN_URL"))
        self.assertTrue(hasattr(settings, "GOOGLE_CLIENT_ID"))
        self.assertTrue(hasattr(settings, "GOOGLE_CLIENT_SECRET"))
        self.assertTrue(hasattr(settings, "REDIRECT_URI"))
