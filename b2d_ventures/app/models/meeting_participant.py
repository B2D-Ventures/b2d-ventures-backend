from django.db import models

from b2d_ventures.app.models import Investor, Startup, Meeting
from b2d_ventures.utils.model_abstracts import AbstractModel


class MeetingParticipant(AbstractModel):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="participants"
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, null=True, blank=True
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Participant for Meeting {self.meeting.id}"

    class Meta:
        app_label = "app"
        unique_together = ("meeting", "investor", "startup")
