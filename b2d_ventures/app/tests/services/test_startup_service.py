from unittest.mock import patch, MagicMock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status

from b2d_ventures.app.models import Startup, Deal, Investment
from b2d_ventures.app.services import StartupService


class StartupServiceTestCase(TestCase):
    """Test case for the StartupService class."""

    def setUp(self):
        """Set up the test environment."""
        self.startup = Startup.objects.create(
            email="startup@example.com",
            username="teststartup",
            name="Test Startup",
            description="A test startup",
        )
        self.deal = Deal.objects.create(
            name="Test Deal",
            startup=self.startup,
            status="approved",
            minimum_investment=1000,
        )

    def test_get_profile(self):
        """Test getting a startup's profile."""
        response = StartupService.get_profile(self.startup.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_get_nonexistent_profile(self):
        """Test getting a profile for a non-existent startup."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.get_profile(9999)

    @patch("b2d_ventures.app.serializers.StartupSerializer")
    def test_update_profile(self, mock_serializer):
        """Test updating a startup's profile."""
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {"name": "Updated Startup"}
        attributes = {"name": "Updated Startup"}

        response = StartupService.update_profile(self.startup.id, attributes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_update_profile_nonexistent_startup(self):
        """Test updating a profile for a non-existent startup."""
        attributes = {"name": "Updated Startup"}
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.update_profile(9999, attributes)

    def test_list_deals(self):
        """Test listing startup's deals."""
        response = StartupService.list_deals(self.startup.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_deals_nonexistent_startup(self):
        """Test listing deals for a non-existent startup."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.list_deals(9999)

    @patch("b2d_ventures.app.serializers.DealSerializer")
    def test_create_deal(self, mock_serializer):
        """Test creating a new deal."""
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {"id": self.deal.id, "name": "New Deal"}
        attributes = {
            "name": "New Deal",
            "minimum_investment": 1000,
            "startup_id": self.startup.id,
        }

        response = StartupService.create_deal(self.startup.id, attributes)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("attributes", response.data)
        self.assertEqual(response.data["attributes"]["name"], "New Deal")

    @patch("b2d_ventures.app.serializers.DealSerializer")
    def test_update_deal(self, mock_serializer):
        """Test updating a specific deal."""
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {"name": "Updated Deal"}
        attributes = {"name": "Updated Deal"}

        response = StartupService.update_deal(self.startup.id, self.deal.id, attributes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_create_deal_nonexistent_startup(self):
        """Test creating a deal for a non-existent startup."""
        attributes = {"name": "New Deal", "minimum_investment": 1000}
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.create_deal(9999, attributes)

    def test_get_deal_details(self):
        """Test getting details of a specific deal."""
        response = StartupService.get_deal_details(self.startup.id, self.deal.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_get_deal_details_nonexistent_startup(self):
        """Test getting deal details for a non-existent startup."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.get_deal_details(9999, self.deal.id)

    def test_get_deal_details_nonexistent_deal(self):
        """Test getting details of a non-existent deal."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.get_deal_details(self.startup.id, 9999)

    def test_update_deal_nonexistent_startup(self):
        """Test updating a deal for a non-existent startup."""
        attributes = {"name": "Updated Deal"}
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.update_deal(9999, self.deal.id, attributes)

    def test_update_deal_nonexistent_deal(self):
        """Test updating a non-existent deal."""
        attributes = {"name": "Updated Deal"}
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.update_deal(self.startup.id, 9999, attributes)

    def test_delete_deal(self):
        """Test deleting a specific deal."""
        response = StartupService.delete_deal(self.startup.id, self.deal.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_deal_nonexistent_startup(self):
        """Test deleting a deal for a non-existent startup."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.delete_deal(9999, self.deal.id)

    def test_delete_deal_nonexistent_deal(self):
        """Test deleting a non-existent deal."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.delete_deal(self.startup.id, 9999)

    def test_list_investments(self):
        """Test listing investments in the startup."""
        investment = Investment.objects.create(
            deal=self.deal, investor=self.startup, investment_amount=1000
        )
        response = StartupService.list_investments(self.startup.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_investments_nonexistent_startup(self):
        """Test listing investments for a non-existent startup."""
        with self.assertRaises(ObjectDoesNotExist):
            StartupService.list_investments(9999)
