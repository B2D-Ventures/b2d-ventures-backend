from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Investor(User):
    """
    Investor model for users who can invest in startups.
    """

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investors"

    available_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def invest(self, amount):
        if amount > self.available_funds:
            raise ValidationError(_("Insufficient funds for investment."))
        self.available_funds -= amount
        self.total_invested += amount
        self.save()

    def add_funds(self, amount):
        if amount < 0:
            raise ValidationError(_("Cannot add negative funds."))
        self.available_funds += amount
        self.save()

    def clean(self):
        if self.available_funds < 0:
            raise ValidationError(_("Available funds cannot be negative."))
        if self.total_invested < 0:
            raise ValidationError(_("Total invested cannot be negative."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
