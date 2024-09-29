from datetime import datetime, timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from b2d_ventures.app.services.authorization_service import AuthorizationService


class CalendarError(Exception):
    """Custom Exception for calendar-related errors."""


class CalendarService:
    @staticmethod
    def get_service(credentials):
        """
        Create and return a Google Calendar service object.

        :param credentials: OAuth2 credentials
        :return: Google Calendar service object
        """
        try:
            service = build("calendar", "v3", credentials=credentials)
            return service
        except Exception as e:
            raise CalendarError(f"Failed to build calendar service: {str(e)}")

    @staticmethod
    def check_availability(service, calendar_id, start_time, end_time):
        """
        Check if a given time slot is available in the calendar.

        :param service: Google Calendar service object
        :param calendar_id: ID of the calendar to check (usually 'primary')
        :param start_time: Start time of the slot to check
        :param end_time: End time of the slot to check
        :return: Boolean indicating if the slot is available
        """
        try:
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)

            time_min = start_time.isoformat()
            time_max = end_time.isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            return len(events) == 0
        except HttpError as error:
            if error.resp.status == 400:
                error_details = error.error_details
                raise CalendarError(f"Bad request to Calendar API: {error_details}")
            elif error.resp.status == 401:
                raise CalendarError(
                    "Unauthorized access to Calendar API. Please check your credentials."
                )
            elif error.resp.status == 403:
                raise CalendarError(
                    "Forbidden access to Calendar API. Please check your permissions."
                )
            else:
                raise CalendarError(
                    f"An error occurred while checking availability: {error}"
                )
        except Exception as e:
            raise CalendarError(
                f"Unexpected error while checking availability: {str(e)}"
            )

    @staticmethod
    def schedule_meeting(
        service, calendar_id, summary, description, start_time, end_time, attendees
    ):
        """
        Schedule a meeting in the calendar.

        :param service: Google Calendar service object
        :param calendar_id: ID of the calendar to add the event to (usually 'primary')
        :param summary: Title of the event
        :param description: Description of the event
        :param start_time: Start time of the event
        :param end_time: End time of the event
        :param attendees: List of attendee email addresses
        :return: The created event object
        """
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
            "attendees": [{"email": attendee} for attendee in attendees],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        try:
            event = (
                service.events()
                .insert(calendarId=calendar_id, body=event, sendUpdates="all")
                .execute()
            )
            return event
        except HttpError as error:
            raise CalendarError(
                f"An error occurred while scheduling the meeting: {error}"
            )

    @staticmethod
    def get_free_busy(service, time_min, time_max, calendars):
        """
        Get the free/busy information for a list of calendars.

        :param service: Google Calendar service object
        :param time_min: Start time for the query
        :param time_max: End time for the query
        :param calendars: List of calendar IDs to check
        :return: Dictionary with free/busy information
        """
        body = {
            "timeMin": time_min.isoformat() + "Z",
            "timeMax": time_max.isoformat() + "Z",
            "items": [{"id": calendar} for calendar in calendars],
        }
        try:
            return service.freebusy().query(body=body).execute()
        except HttpError as error:
            raise CalendarError(
                f"An error occurred while getting free/busy information: {error}"
            )

    @staticmethod
    def schedule_investor_startup_meeting(
        token, title, description, start_time, end_time, startup_email
    ):
        """
        Schedule a meeting between an investor and a startup.

        :param token: Token containing the authorization token
        :param title: Title of the event
        :param description: Description of the event
        :param start_time: Start time of the event
        :param end_time: End time of the event
        :param startup_email: Email address of the startup
        :return: The created event object
        """
        try:
            credentials = Credentials(token=token)
            service = CalendarService.get_service(credentials)

            if not CalendarService.check_availability(
                service, "primary", start_time, end_time
            ):
                raise CalendarError(
                    "The requested time slot is not available for the investor"
                )

            event = CalendarService.schedule_meeting(
                service,
                "primary",
                title,
                description,
                start_time,
                end_time,
                [startup_email],
            )

            return event

        except Exception as e:
            raise CalendarError(f"Error scheduling investor-startup meeting: {str(e)}")
