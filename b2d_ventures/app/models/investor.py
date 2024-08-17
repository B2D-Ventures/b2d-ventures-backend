from django.db import models
from .user import User


class Investor(User):
    available_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)
