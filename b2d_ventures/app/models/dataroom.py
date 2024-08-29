from django.contrib.auth import get_user_model
from django.db import models

from b2d_ventures.app.models.abstract_model import AbstractModel

User = get_user_model()


class DataRoom(AbstractModel):
    startup = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="data_room"
    )
    data_room_pdf = models.FileField(
        upload_to="data_room_pdfs/",
        null=True,
        blank=True,
        help_text="Upload a PDF containing all data room information"
    )
    access_permissions = models.TextField(
        blank=True,
        help_text="Specify access permissions for this data room"
    )

    def __str__(self):
        return f"DataRoom for {self.startup.username}"
