from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField

from b2d_ventures.app.models.abstract_model import AbstractModel


class User(AbstractUser, AbstractModel):
    class Meta:
        app_label = "app"

    TYPE_CHOICES = (
        ("admin", "Admin"),
        ("investor", "Investor"),
        ("startup", "Startup"),
        ("unassigned", "Unassigned"),
    )

    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    role = models.CharField(max_length=20, choices=TYPE_CHOICES, default="unassigned")
    refresh_token = EncryptedCharField(
        max_length=150, null=True, default="", blank=True
    )
