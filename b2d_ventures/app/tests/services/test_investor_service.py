from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status

from b2d_ventures.app.models import Investor, Deal, Investment, Startup
from b2d_ventures.app.services import InvestorService, InvestorError


class InvestorServiceTestCase(TestCase):
    """Test case for the InvestorService class."""

    def setUp(self):
        """Set up the test environment."""
        self.investor = Investor.objects.create(
            email="investor@example.com",
            username="investor",
            total_invested=0,
            refresh_token="mock_refresh_token",
        )
        self.startup = Startup.objects.create(
            email="startup@example.com",
            username="startup",
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
        """Test getting an investor's profile."""
        response = InvestorService.get_profile(self.investor.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_get_nonexistent_profile(self):
        """Test getting a profile for a non-existent investor."""
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.get_profile(9999)

    def test_list_investments(self):
        """Test listing investments made by the investor."""
        investment = Investment.objects.create(
            deal=self.deal, investor=self.investor,
            investment_amount=Decimal("1500.00")
        )
        response = InvestorService.list_investments(self.investor.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_investments_nonexistent_investor(self):
        """Test listing investments for a non-existent investor."""
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.list_investments(9999)

    @patch(
        "b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_create_investment(self, mock_email):
        """Test creating a new investment."""
        mock_email.return_value = "email"
        attributes = {"investment_amount": 2000}
        response = InvestorService.create_investment(
            self.investor.id, self.deal.id, attributes
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("attributes", response.data)
        self.assertEqual(response.data["attributes"]["investment_amount"],
                         "2000.00")

    def test_create_investment_below_minimum(self):
        """Test creating an investment below the minimum amount."""
        attributes = {"investment_amount": 500}
        with self.assertRaises(InvestorError):
            InvestorService.create_investment(
                self.investor.id, self.deal.id, attributes
            )

    def test_create_investment_nonexistent_investor(self):
        """Test creating an investment for a non-existent investor."""
        attributes = {"investment_amount": 2000}
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.create_investment(9999, self.deal.id, attributes)

    def test_create_investment_nonexistent_deal(self):
        """Test creating an investment for a non-existent deal."""
        attributes = {"investment_amount": 2000}
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.create_investment(self.investor.id, 9999,
                                              attributes)

    def test_get_investment(self):
        """Test getting details of a specific investment."""
        investment = Investment.objects.create(
            deal=self.deal, investor=self.investor,
            investment_amount=Decimal("1500.00")
        )
        response = InvestorService.get_investment(self.investor.id,
                                                  investment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)

    def test_get_investment_nonexistent_investor(self):
        """Test getting an investment for a non-existent investor."""
        investment = Investment.objects.create(
            deal=self.deal, investor=self.investor,
            investment_amount=Decimal("1500.00")
        )
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.get_investment(9999, investment.id)

    def test_get_investment_nonexistent_investment(self):
        """Test getting a non-existent investment."""
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.get_investment(self.investor.id, 9999)

    @patch(
        "b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_request_dataroom(self, mock_email):
        """Test requesting access to a deal's dataroom."""
        mock_email = "email"
        self.deal.dataroom = "path/to/dataroom.pdf"
        self.deal.save()
        response = InvestorService.request_dataroom(self.investor.id,
                                                    self.deal.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Dataroom sent successfully to your email"
        )

    def test_request_dataroom_no_file(self):
        """Test requesting a dataroom when no file is available."""
        with self.assertRaises(InvestorError):
            InvestorService.request_dataroom(self.investor.id, self.deal.id)

    def test_schedule_meeting(self):
        """Test scheduling a meeting between an investor and a startup."""
        attributes = {
            "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(days=1,
                                                    hours=1)).isoformat(),
            "title": "Investor-Startup Meeting",
            "description": "Discuss investment opportunities",
        }
        with patch(
                "b2d_ventures.app.services.AuthService.refresh_access_token"
        ) as mock_refresh:
            mock_refresh.return_value = "mock_access_token"
            with patch(
                    "b2d_ventures.app.services.CalendarService.schedule_investor_startup_meeting"
            ) as mock_schedule:
                mock_schedule.return_value = {"id": "mock_event_id"}
                response = InvestorService.schedule_meeting(
                    self.investor.id, self.startup.id, attributes
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIn("attributes", response.data)

    def test_schedule_meeting_nonexistent_investor(self):
        """Test scheduling a meeting for a non-existent investor."""
        attributes = {
            "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(days=1,
                                                    hours=1)).isoformat(),
        }
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.schedule_meeting(9999, self.startup.id, attributes)

    def test_schedule_meeting_nonexistent_startup(self):
        """Test scheduling a meeting for a non-existent startup."""
        attributes = {
            "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(days=1,
                                                    hours=1)).isoformat(),
        }
        with self.assertRaises(ObjectDoesNotExist):
            InvestorService.schedule_meeting(self.investor.id, 9999,
                                             attributes)

    def test_schedule_meeting_no_refresh_token(self):
        """Test scheduling a meeting when the investor has no refresh token."""
        self.investor.refresh_token = None
        self.investor.save()
        attributes = {
            "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(days=1,
                                                    hours=1)).isoformat(),
        }
        with self.assertRaises(InvestorError):
            InvestorService.schedule_meeting(
                self.investor.id, self.startup.id, attributes
            )
