from django.db import models
from django.contrib.auth.models import AbstractUser
from b2d_ventures.utils.model_abstracts import AbstractModel


class User(AbstractUser, AbstractModel):
    class Meta:
        app_label = "app"

    token = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def user_type(self):
        if hasattr(self, "admin"):
            return "Admin"
        elif hasattr(self, "investor"):
            return "Investor"
        elif hasattr(self, "startup"):
            return "Startup"
        return "Unknown"
