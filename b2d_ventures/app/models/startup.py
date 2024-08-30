from django.db import models
from .user import User


class Startup(User):
    name = models.CharField(max_length=255)
    description = models.TextField()
    fundraising_goal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'startup'
        super().save(*args, **kwargs)
