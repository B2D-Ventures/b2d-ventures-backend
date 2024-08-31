from django.db import models
from .user import User


class Admin(User):
    permission = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = "admin"
        super().save(*args, **kwargs)
