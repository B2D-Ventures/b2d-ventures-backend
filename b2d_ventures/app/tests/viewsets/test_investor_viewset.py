from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from b2d_ventures.app.models import Investor, Deal, Meeting, Investment, Startup

User = get_user_model()


class InvestorViewSetTest(APITestCase):
    """
    Test suite for the InvestorViewSet.

    This class contains tests for investor-related operations such as getting profiles,
    listing investments, creating investments, and scheduling meetings.
    """

    def setUp(self):
        """
        Set up test data for the InvestorViewSet tests.
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

        self.investor = Investor.objects.create(
            email="investor@example.com",
            username="Investor User",
            available_funds=10000,
            total_invested=0,
            refresh_token="test_token",
            password="investorpass",
        )
        self.investor.set_password("investorpass")
        self.investor.save()
        self.client.force_authenticate(user=self.investor)

    def test_get_profile(self):
        """Test getting the investor's profile."""
        url = f"/api/investor/{self.investor.id}/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)
        self.assertEqual(response.data["attributes"]["email"], self.investor.email)

    def test_get_profile_not_found(self):
        """Test getting a profile for a non-existent investor."""
        url = "/api/investor/00000000-0000-0000-0000-000000000000/profile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_investments(self):
        """Test listing investments made by the investor."""
        url = f"/api/investor/{self.investor.id}/investments/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
            raised=0,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
        )
        Investment.objects.create(
            deal=deal,
            investor=self.investor,
            investment_amount=5000,
        )

        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_create_investment(self, mock_email):
        """Test creating a new investment."""
        mock_email.return_value = "email"
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
            raised=0,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
            status="approved",
        )
        url = f"/api/investor/{self.investor.id}/investments/{deal.id}/"
        data = {
            "data": {
                "attributes": {
                    "investment_amount": 5000,
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Investment.objects.count(), 1)
        investment = Investment.objects.get()
        self.assertEqual(investment.investment_amount, 5000)
        self.assertEqual(investment.deal, deal)

    @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_create_investment_invalid_amount(self, mock_email):
        """Test creating an investment with amount below minimum investment."""
        mock_email.return_value = "email"
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=1000,
            raised=0,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
            status="approved",
        )

        url = f"/api/investor/{self.investor.id}/investments/{deal.id}/"
        data = {
            "data": {
                "attributes": {
                    "investment_amount": 500,
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    def test_create_investment_invalid_deal(self, mock_email):
        """Test creating an investment for a non-existent deal."""
        mock_email.return_value = "email"
        url = f"/api/investor/{self.investor.id}/investments/00000000-0000-0000-0000-000000000000/"
        data = {
            "data": {
                "attributes": {
                    "investment_amount": 5000,
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # @patch("b2d_ventures.utils.email_service.EmailService.send_email_with_attachment")
    # def test_request_dataroom(self, mock_email):
    #     """Test requesting access to a deal's dataroom."""
    #     mock_email.return_value = "email"
    #     mock_pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/MediaBox [0 0 300 144]\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Times-Roman\n>>\nendobj\n5 0 obj\n<< /Length 55 >>\nstream\nBT\n/F1 18 Tf\n0 0 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000274 00000 n \n0000000342 00000 n \ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n447\n%%EOF"
    #     mock_pdf = ContentFile(mock_pdf_content, name="test.pdf")
    #     deal = Deal.objects.create(
    #         startup=self.startup,
    #         name="Test Deal",
    #         allocation=10000,
    #         price_per_unit=100,
    #         minimum_investment=1000,
    #         raised=0,
    #         start_date=timezone.now(),
    #         end_date=timezone.now() + timezone.timedelta(days=30),
    #         status="approved",
    #         dataroom=mock_pdf,
    #     )
    #
    #     url = f"/api/investor/{self.investor.id}/deals/{deal.id}/request-dataroom/"
    #     response = self.client.post(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("b2d_ventures.app.services.auth_service.AuthService.refresh_access_token")
    @patch(
        "b2d_ventures.app.services.calendar_service.CalendarService.schedule_investor_startup_meeting"
    )
    def test_schedule_meeting(self, schedule_meeting, refresh_access_token):
        """Test scheduling a meeting with a startup."""
        refresh_access_token.return_value = "token"
        schedule_meeting.return_value = {"id": "mock_id"}
        url = f"/api/investor/{self.investor.id}/schedule-meeting/{self.startup.id}/"
        data = {
            "data": {
                "attributes": {
                    "title": "Meeting with Startup",
                    "description": "Discuss investment opportunities",
                    "start_time": timezone.now().isoformat(),
                    "end_time": (
                        timezone.now() + timezone.timedelta(hours=1)
                    ).isoformat(),
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 1)
        meeting = Meeting.objects.first()
        self.assertEqual(meeting.title, "Meeting with Startup")
        self.assertEqual(meeting.investor, self.investor)
        self.assertEqual(meeting.startup, self.startup)

    def test_schedule_meeting_invalid_startup(self):
        """Test scheduling a meeting with a non-existent startup."""
        url = f"/api/investor/{self.investor.id}/schedule-meeting/00000000-0000-0000-0000-000000000000/"
        data = {
            "data": {
                "attributes": {
                    "title": "Meeting with Startup",
                    "description": "Discuss investment opportunities",
                    "start_time": timezone.now().isoformat(),
                    "end_time": (
                        timezone.now() + timezone.timedelta(hours=1)
                    ).isoformat(),
                }
            }
        }
        response = self.client.post(url, data, format="vnd.api+json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_meetings(self):
        """Test getting all meetings that belong to the investor."""

        Meeting.objects.create(
            investor=self.investor,
            startup=self.startup,
            title="First Meeting",
            description="First meeting description",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
        )
        Meeting.objects.create(
            investor=self.investor,
            startup=self.startup,
            title="Second Meeting",
            description="Second meeting description",
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
        )

        url = f"/api/investor/{self.investor.id}/meetings/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_dashboard(self):
        """Test getting the investor's dashboard."""
        deal = Deal.objects.create(
            startup=self.startup,
            name="Test Deal",
            allocation=10000,
            price_per_unit=100,
            minimum_investment=500,
            raised=0,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
            status="approved",
        )
        investment = Investment.objects.create(
            deal=deal,
            investor=self.investor,
            investment_amount=5000,
        )

        Meeting.objects.create(
            investor=self.investor,
            startup=self.startup,
            title="Meeting with Startup",
            description="Discuss investment opportunities",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
        )

        url = f"/api/investor/{self.investor.id}/dashboard/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attributes", response.data)
        self.assertIn("profile", response.data["attributes"])
        self.assertIn("investments", response.data["attributes"])
        self.assertIn("meetings", response.data["attributes"])

        self.assertEqual(response.data["attributes"]["investment_count"], 1)
        self.assertEqual(
            response.data["attributes"]["investments"][0]["attributes"]["id"],
            str(investment.id),
        )
        self.assertEqual(len(response.data["attributes"]["meetings"]), 1)
