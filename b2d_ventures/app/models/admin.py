from django.db import models
from django.contrib.auth.models import User


class Admin(User):
    """
    Admin model for users with administrative privileges.
    """

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    permission = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """Save the user instance."""
        if not self.pk:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)
