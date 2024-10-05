from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from b2d_ventures.app.models import (
    Admin,
    User,
    Deal,
    Investment,
    Meeting,
    Startup,
    Investor,
)

User = get_user_model()


class AdminViewSetTest(APITestCase):
    """
    Test suite for the AdminViewSet.

    This class contains tests for various admin operations including user management,
    deal operations, investment tracking, and meeting scheduling.
    """

    def setUp(self):
        """
        Set up test data for the AdminViewSet tests.
        """

        self.admin_user = Admin.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            role="admin",
        )
        self.client.force_authenticate(user=self.admin_user)

        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="user1pass",
            role="unassigned",
        )

        self.startup_user = Startup.objects.create_user(
            username="startup",
            email="startup@example.com",
            password="startuppass",
            role="startup",
            name="Startup 1",
            description="A test startup",
            fundraising_goal=100000,
        )

        self.investor_user = Investor.objects.create_user(
            username="investor",
            email="investor@example.com",
            password="investorpass",
            role="investor",
            available_funds=50000,
        )

        self.deal = Deal.objects.create(
            startup=self.startup_user,
            name="Deal 1",
            description="A test deal",
            allocation=50000.00,
            price_per_unit=100.00,
            minimum_investment=1000.00,
            type="Equity",
            raised=0.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
            status="pending",
        )

        self.investment = Investment.objects.create(
            deal=self.deal, investor=self.investor_user, investment_amount=10000.00
        )

        self.meeting = Meeting.objects.create(
            investor=self.investor_user,
            startup=self.startup_user,
            title="Investor-Startup Meeting",
            description="Discuss investment opportunities",
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
        )

    def test_list_users(self):
        """Test listing all users."""
        url = "/api/admin/users/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), User.objects.count())

    def test_delete_user(self):
        """Test deleting a user."""
        url = f"/api/admin/{self.user1.pk}/users/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user1.pk)

    def test_list_deals(self):
        """Test listing all deals."""
        url = "/api/admin/deals/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), Deal.objects.count())

    @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_approve_deal(self, mock_email):
        """Test approving a deal."""
        mock_email.return_value = "email"
        url = f"/api/admin/{self.deal.pk}/deals/"
        data = {"data": {"attributes": {"action": "approve"}}}
        response = self.client.put(url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.status, "approved")

    @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_reject_deal(self, mock_email):
        """Test rejecting a deal."""
        mock_email.return_value = "email"
        url = f"/api/admin/{self.deal.pk}/deals/"
        data = {"data": {"attributes": {"action": "reject"}}}
        response = self.client.put(url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.status, "rejected")

    def test_invalid_action_deal(self):
        """Test invalid action on a deal."""
        url = f"/api/admin/{self.deal.pk}/deals/"
        data = {"data": {"attributes": {"action": "invalid_action"}}}
        response = self.client.put(url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_deal(self):
        """Test deleting a deal."""
        url = f"/api/admin/{self.deal.pk}/deals/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Deal.DoesNotExist):
            Deal.objects.get(pk=self.deal.pk)

    def test_list_investments(self):
        """Test listing all investments."""
        url = "/api/admin/investments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), Investment.objects.count())

    def test_delete_investment(self):
        """Test deleting an investment."""
        url = f"/api/admin/{self.investment.pk}/investments/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Investment.DoesNotExist):
            Investment.objects.get(pk=self.investment.pk)

    def test_list_meetings(self):
        """Test listing all meetings."""
        url = "/api/admin/meetings/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data.get("data"), list))
        self.assertEqual(len(response.data.get("data")), Meeting.objects.count())

    def test_dashboard(self):
        """Test retrieving the admin dashboard."""
        url = "/api/admin/dashboard/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
