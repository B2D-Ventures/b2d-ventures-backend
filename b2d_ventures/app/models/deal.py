from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from b2d_ventures.app.models import Startup
from b2d_ventures.app.models.abstract_model import AbstractModel


def dataroom_upload_path(instance, filename):
    return f"datarooms/{instance.startup.name}/{filename}"


class Deal(AbstractModel):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="deals")
    name = models.CharField(max_length=255, default="")
    content = models.TextField(default="")
    image_background_url = models.URLField(max_length=255, default="")
    image_logo_url = models.URLField(max_length=255, default="")
    image_content_url = models.URLField(max_length=255, default="")
    allocation = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_investment = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )
    type = models.TextField(default="")
    raised = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    investor_count = models.PositiveIntegerField(default=0)
    dataroom = models.FileField(
        upload_to=dataroom_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )
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
