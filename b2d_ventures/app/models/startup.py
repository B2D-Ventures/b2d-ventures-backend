from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class Startup(User):
    """
    Startup model for users representing startups that can receive investments.
    """

    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"

    name = models.CharField(max_length=255)
    description = models.TextField()
    fundraising_goal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def add_investment(self, amount):
        if amount < 0:
            raise ValidationError(_("Cannot add negative investment."))
        self.total_raised += amount
        self.save()

    def clean(self):
        if self.total_raised < 0:
            raise ValidationError(_("Total raised cannot be negative."))
        if self.total_raised > self.fundraising_goal:
            raise ValidationError(_("Total raised cannot exceed fundraising goal."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
