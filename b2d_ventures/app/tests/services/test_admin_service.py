from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist

from b2d_ventures.app.models import User, Deal, Investment, Meeting, Investor, Startup
from b2d_ventures.app.services import AdminService


class AdminServiceTestCase(TestCase):
    """Test case for the AdminService class."""

    def setUp(self):
        """Set up the test environment."""
        self.service = AdminService()

    def test_list_users(self):
        """Test listing all users."""
        User.objects.create(email="user1@example.com", username="user1")
        User.objects.create(email="user2@example.com", username="user2")
        users = self.service.list_users()
        self.assertEqual(users.count(), 2)

    def test_get_user_details(self):
        """Test retrieving details of a specific user."""
        user = User.objects.create(email="user@example.com", username="user")
        retrieved_user = self.service.get_user_details(user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_nonexistent_user_details(self):
        """Test retrieving details of a non-existent user."""
        with self.assertRaises(ObjectDoesNotExist):
            self.service.get_user_details("00000000-0000-0000-0000-000000000000")

    def test_list_deals(self):
        """Test listing all deals."""
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        Deal.objects.create(name="Deal 1", startup=startup)
        Deal.objects.create(name="Deal 2", startup=startup)
        deals = self.service.list_deals()
        self.assertEqual(deals.count(), 2)

    @patch("b2d_ventures.utils.EmailService.send_email_with_attachment")
    def test_approve_deal(self, mock_send_email):
        """Test approving a deal."""
        mock_send_email.return_value = True
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        deal = Deal.objects.create(name="Test Deal", status="pending", startup=startup)
        approved_deal = self.service.approve_deal(deal.id)
        self.assertEqual(approved_deal.status, "approved")

    @patch("b2d_ventures.utils.EmailService.send_email_with_attachment")
    def test_reject_deal(self, mock_send_email):
        """Test rejecting a deal."""
        mock_send_email.return_value = True
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        deal = Deal.objects.create(name="Test Deal", status="pending", startup=startup)
        rejected_deal = self.service.reject_deal(deal.id)
        self.assertEqual(rejected_deal.status, "rejected")

    def test_list_investments(self):
        """Test listing all investments."""
        investor = Investor.objects.create(
            email="investor@example.com", username="investor"
        )
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        deal = Deal.objects.create(name="Test Deal", startup=startup)
        Investment.objects.create(deal=deal, investor=investor, investment_amount=1000)
        Investment.objects.create(deal=deal, investor=investor, investment_amount=2000)
        investments = self.service.list_investments()
        self.assertEqual(investments.count(), 2)

    def test_list_meetings(self):
        """Test listing all meetings."""
        investor = Investor.objects.create(
            email="investor@example.com", username="investor"
        )
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        Meeting.objects.create(investor=investor, startup=startup)
        Meeting.objects.create(investor=investor, startup=startup)
        meetings = self.service.list_meetings()
        self.assertEqual(meetings.count(), 2)

    def test_get_dashboard_data(self):
        """Test retrieving dashboard data."""
        User.objects.create(email="user@example.com", username="user")
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        Deal.objects.create(name="Deal", status="active", startup=startup)
        investor = Investor.objects.create(
            email="investor@example.com", username="investor"
        )
        deal = Deal.objects.create(name="Test Deal", startup=startup)
        Investment.objects.create(deal=deal, investor=investor, investment_amount=1000)
        Meeting.objects.create(
            investor=investor,
            startup=startup,
            start_time=timezone.now() + timezone.timedelta(days=1),
        )

        dashboard_data = self.service.get_dashboard_data()
        self.assertIn("total_users", dashboard_data)
        self.assertIn("total_deals", dashboard_data)
        self.assertIn("active_deals", dashboard_data)
        self.assertIn("total_investments", dashboard_data)
        self.assertIn("total_investment_amount", dashboard_data)
        self.assertIn("total_meetings", dashboard_data)
        self.assertIn("upcoming_meetings", dashboard_data)

    def test_delete_user(self):
        """Test deleting a user."""
        user = User.objects.create(email="user@example.com", username="user")
        self.service.delete_user(user.id)
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_delete_nonexistent_user(self):
        """Test deleting a non-existent user."""
        with self.assertRaises(ObjectDoesNotExist):
            self.service.delete_user("00000000-0000-0000-0000-000000000000")

    def test_delete_meeting(self):
        """Test deleting a meeting."""
        investor = Investor.objects.create(
            email="investor@example.com", username="investor"
        )
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        meeting = Meeting.objects.create(investor=investor, startup=startup)
        self.service.delete_meeting(meeting.id)
        self.assertFalse(Meeting.objects.filter(id=meeting.id).exists())

    def test_delete_investment(self):
        """Test deleting an investment."""
        investor = Investor.objects.create(
            email="investor@example.com", username="investor"
        )
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        deal = Deal.objects.create(name="Test Deal", startup=startup)
        investment = Investment.objects.create(
            deal=deal, investor=investor, investment_amount=1000
        )
        self.service.delete_investment(investment.id)
        self.assertFalse(Investment.objects.filter(id=investment.id).exists())

    def test_delete_deal(self):
        """Test deleting a deal."""
        startup = Startup.objects.create(
            name="Test Startup", email="startup@example.com", username="teststartup"
        )
        deal = Deal.objects.create(name="Test Deal", startup=startup)
        self.service.delete_deal(deal.id)
        self.assertFalse(Deal.objects.filter(id=deal.id).exists())
