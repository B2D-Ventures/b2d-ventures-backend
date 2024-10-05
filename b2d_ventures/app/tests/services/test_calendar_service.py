from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from django.test import TestCase
from googleapiclient.errors import HttpError

from b2d_ventures.app.services import CalendarService, CalendarError


class CalendarServiceTestCase(TestCase):
    """Test case for the CalendarService class."""

    def setUp(self):
        """Set up the test environment."""
        self.service = CalendarService()
        self.credentials = MagicMock()  # Mocking the credentials

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_check_availability(self, mock_get_service):
        """Test checking availability in the calendar."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        calendar_id = "primary"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)

        mock_service.events().list().execute.return_value = {"items": []}
        available = self.service.check_availability(
            mock_service, calendar_id, start_time, end_time
        )
        self.assertTrue(available)

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_check_availability_with_events(self, mock_get_service):
        """Test checking availability when events are present."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        calendar_id = "primary"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)

        mock_service.events().list().execute.return_value = {"items": [{"id": "1"}]}
        available = self.service.check_availability(
            mock_service, calendar_id, start_time, end_time
        )
        self.assertFalse(available)

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_schedule_meeting(self, mock_get_service):
        """Test scheduling a meeting in the calendar."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        calendar_id = "primary"
        summary = "Test Meeting"
        description = "Meeting Description"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        attendees = ["attendee@example.com"]

        mock_service.events().insert().execute.return_value = {"id": "event_id"}
        event = self.service.schedule_meeting(
            mock_service,
            calendar_id,
            summary,
            description,
            start_time,
            end_time,
            attendees,
        )
        self.assertEqual(event["id"], "event_id")

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_schedule_meeting_http_error(self, mock_get_service):
        """Test scheduling a meeting and handling HttpError."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        calendar_id = "primary"
        summary = "Test Meeting"
        description = "Meeting Description"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        attendees = ["attendee@example.com"]

        mock_service.events().insert().execute.side_effect = HttpError(
            resp=MagicMock(status=400), content=b"Bad Request"
        )
        with self.assertRaises(CalendarError):
            self.service.schedule_meeting(
                mock_service,
                calendar_id,
                summary,
                description,
                start_time,
                end_time,
                attendees,
            )

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_get_free_busy(self, mock_get_service):
        """Test getting free/busy information."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        time_min = datetime.now(timezone.utc)
        time_max = time_min + timedelta(days=1)
        calendars = ["primary"]

        mock_service.freebusy().query().execute.return_value = {
            "calendars": {"primary": {"busy": []}}
        }
        free_busy_info = self.service.get_free_busy(
            mock_service, time_min, time_max, calendars
        )
        self.assertIn("calendars", free_busy_info)

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_schedule_investor_startup_meeting(self, mock_get_service):
        """Test scheduling a meeting between an investor and a startup."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        token = "mock_token"
        title = "Investor-Startup Meeting"
        description = "Meeting Description"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        startup_email = "startup@example.com"

        mock_service.events().insert().execute.return_value = {"id": "event_id"}
        event = self.service.schedule_investor_startup_meeting(
            token, title, description, start_time, end_time, startup_email
        )
        self.assertEqual(event["id"], "event_id")

    @patch("b2d_ventures.app.services.CalendarService.get_service")
    def test_schedule_investor_startup_meeting_availability_error(
        self, mock_get_service
    ):
        """Test scheduling a meeting and handling availability error."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        token = "mock_token"
        title = "Investor-Startup Meeting"
        description = "Meeting Description"
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        startup_email = "startup@example.com"

        mock_service.events().list().execute.return_value = {"items": [{"id": "1"}]}

        with self.assertRaises(CalendarError):
            self.service.schedule_investor_startup_meeting(
                token, title, description, start_time, end_time, startup_email
            )
