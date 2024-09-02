from django.db import models

from b2d_ventures.app.models import User, Deal
from b2d_ventures.app.models.abstract_model import AbstractModel


class Investment(AbstractModel):
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="deal_investors"
    )
    investor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="deal_investments"
    )
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.investor.username} - {self.deal.name} - ${self.investment_amount}"
        )

    class Meta:
        app_label = "app"
