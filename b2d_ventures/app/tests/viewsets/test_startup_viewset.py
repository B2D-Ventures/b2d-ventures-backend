from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from b2d_ventures.app.models import Startup, Deal, Meeting, Investment, \
    Investor
from b2d_ventures.app.services import StartupError

User = get_user_model()


class StartupViewSetTest(APITestCase):
    """
    Test suite for the StartupViewSet.

    This class contains tests for startup-related operations such as getting profiles,
    listing deals, creating deals, updating deals, deleting deals, listing investments,
    listing meetings, and getting the startup dashboard.
    """

    def setUp(self):
        """
        Set up test data for the StartupViewSet tests.
        """
        self.startup = Startup.objects.create(
            email="startup@example.com",
            username="Startup User",
            name="Test Startup",
            refresh_token="test_token",
            fundraising_goal=50000,
            total_raised=0,
            password="startuppass",
        )
        self.startup.set_password("startuppass")
        self.startup.save()

        self.client.force_authenticate(user=self.startup)

    def test_get_profile(self):
        """
        Test getting the startup's profile.
        """
        url = f"/api/startup/{self.startup.id}/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)
        self.assertEqual(response.data["attributes"]["email"],
                         self.startup.email)

    def test_update_profile(self):
        """
        Test updating the startup's profile.
        """
        url = f"/api/startup/{self.startup.id}/profile/"
        data = {
            "data": {
                "attributes": {
                    "name": "Updated Startup Name",
                    "description": "Updated description",
                }
            }
        }
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["attributes"]["name"],
                         "Updated Startup Name")
        self.assertEqual(
            response.data["attributes"]["description"], "Updated description"
        )

    def test_list_deals(self):
        """
        Test listing deals for the startup.
        """
        Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
            raised=0,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
        )

        url = f"/api/startup/{self.startup.id}/deals/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["attributes"]["name"], "Test Deal")

    def test_create_deal(self):
        """
        Test creating a new deal for the startup using form-data.
        """
        url = f"/api/startup/{self.startup.id}/deals/"

        data = {
            "name": "New Deal",
        }

        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Deal.objects.count(), 1)

        created_deal = Deal.objects.first()
        self.assertIsNotNone(created_deal.image_background)
        self.assertIsNotNone(created_deal.image_logo)
        self.assertIsNotNone(created_deal.image_content)
        self.assertIsNotNone(created_deal.dataroom)

    def test_update_deal(self):
        """
        Test updating an existing deal for the startup.
        """
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
        )

        url = f"/api/startup/{self.startup.id}/deals/{deal.id}/"
        data = {
            "data": {
                "type": "Deal",
                "id": str(deal.id),
                "attributes": {
                    "name": "Updated Deal",
                    "allocation": "15000",
                    "price_per_unit": "150",
                },
            }
        }
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["attributes"]["name"],
                         "Updated Deal")
        self.assertEqual(response.data["data"]["attributes"]["allocation"],
                         "15000.00")
        self.assertEqual(
            response.data["data"]["attributes"]["price_per_unit"], "150.00"
        )

    @patch("b2d_ventures.app.services.StartupService.update_deal")
    def test_update_deal(self, mock_update_deal):
        """
        Test updating an existing deal for the startup.
        """
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
        )

        mock_update_deal.return_value = Response(
            {"attributes": {"name": "Updated Deal"}}, status=status.HTTP_200_OK
        )

        url = f"/api/startup/{self.startup.id}/deals/{deal.id}/"
        data = {
            "data": {
                "attributes": {
                    "name": "Updated Deal",
                }
            }
        }
        response = self.client.put(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["attributes"]["name"], "Updated Deal")

    @patch("b2d_ventures.app.services.StartupService.delete_deal")
    def test_delete_deal(self, mock_delete_deal):
        """
        Test deleting a deal for the startup.
        """
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
        )

        mock_delete_deal.return_value = Response(
            status=status.HTTP_204_NO_CONTENT)

        url = f"/api/startup/{self.startup.id}/deals/{deal.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_investments(self):
        """
        Test listing investments for the startup.
        """
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
        )
        investor = Investor.objects.create(
            email="investor@example.com", username="Investor"
        )
        Investment.objects.create(
            deal=deal,
            investor=investor,
            investment_amount=5000,
        )

        url = f"/api/startup/{self.startup.id}/investments/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["attributes"]["investment_amount"],
                         "5000.00")

    def test_list_meetings(self):
        """
        Test listing meetings for the startup.
        """
        investor = Investor.objects.create(
            email="investor@example.com", username="Investor"
        )
        Meeting.objects.create(
            investor=investor,
            startup=self.startup,
            title="Test Meeting",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
        )

        url = f"/api/startup/{self.startup.id}/meetings/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["attributes"]["title"], "Test Meeting"
        )

    @patch("b2d_ventures.app.services.StartupService.get_profile")
    @patch("b2d_ventures.app.services.StartupService.list_deals")
    @patch("b2d_ventures.app.services.StartupService.list_investments")
    def test_dashboard(self, mock_list_investments, mock_list_deals,
                       mock_get_profile):
        """
        Test getting the startup's dashboard.
        """
        mock_get_profile.return_value = Response(
            {"attributes": {"name": "Test Startup"}}
        )
        mock_list_deals.return_value = Response(
            [{"attributes": {"name": "Test Deal"}}])
        mock_list_investments.return_value = Response(
            [{"attributes": {"investment_amount": "5000.00"}}]
        )

        url = f"/api/startup/{self.startup.id}/dashboard/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)
        self.assertIn("profile", response.data["attributes"])
        self.assertIn("deals", response.data["attributes"])
        self.assertIn("investments", response.data["attributes"])

    def test_get_profile_not_found(self):
        """
        Test getting a profile for a non-existent startup.
        """
        url = "/api/startup/00000000-0000-0000-0000-000000000000/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("b2d_ventures.app.services.StartupService.get_profile")
    def test_get_profile_startup_error(self, mock_get_profile):
        """
        Test getting a profile with a StartupError.
        """
        mock_get_profile.side_effect = StartupError("Test error")

        url = f"/api/startup/{self.startup.id}/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("b2d_ventures.app.services.StartupService.get_profile")
    def test_get_profile_internal_error(self, mock_get_profile):
        """
        Test getting a profile with an internal server error.
        """
        mock_get_profile.side_effect = Exception("Test error")

        url = f"/api/startup/{self.startup.id}/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
