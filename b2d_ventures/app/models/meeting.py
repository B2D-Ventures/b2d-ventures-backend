from django.db import models

from b2d_ventures.app.models import Investor, Startup
from b2d_ventures.app.models.abstract_model import AbstractModel


class Meeting(AbstractModel):
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="meetings"
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name="meetings"
    )
    title = models.CharField(max_length=255, default="Investor-Startup Meeting")
    description = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    investor_event_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Meeting: {self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        app_label = "app"
        ordering = ["-start_time"]
