from django.db import models

from b2d_ventures.app.models import Startup
from b2d_ventures.utils.model_abstracts import AbstractModel


class Deal(AbstractModel):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="deals")
    name = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(max_length=255)
    allocation = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_investment = models.DecimalField(max_digits=15, decimal_places=2)
    raised = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    investor_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("closed", "Closed"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"{self.name} - {self.startup.name}"

    class Meta:
        app_label = "app"
