from django.db import models

from b2d_ventures.app.models import Investor, Startup
from b2d_ventures.app.models.abstract_model import AbstractModel


class Meeting(AbstractModel):
    date = models.DateTimeField()
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, null=True, blank=True
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, null=True, blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
            ("completed", "Completed"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"Meeting on {self.date} - {self.status}"

    class Meta:
        app_label = "app"
