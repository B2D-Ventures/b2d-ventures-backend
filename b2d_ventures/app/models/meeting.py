from django.db import models

from b2d_ventures.utils.model_abstracts import AbstractModel


class Meeting(AbstractModel):
    date = models.DateTimeField()
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
