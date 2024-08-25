from django.contrib.auth.models import AbstractUser
from django.db import models

from b2d_ventures.app.models.abstract_model import AbstractModel


class User(AbstractUser, AbstractModel):
    class Meta:
        app_label = "app"

    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
