from django.db import models
from .user import User


class Investor(User):
    available_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = "investor"
        super().save(*args, **kwargs)
