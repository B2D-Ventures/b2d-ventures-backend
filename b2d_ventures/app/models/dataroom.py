from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DataRoom(models.Model):
    startup = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='data_room')
    income_statement = models.TextField(blank=True)
    balance_sheet = models.TextField(blank=True)
    cash_flow_statement = models.TextField(blank=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                  blank=True)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                 blank=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2,
                                     null=True, blank=True)
    burn_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                    blank=True)
    runway = models.IntegerField(null=True, blank=True)
    current_valuation = models.DecimalField(max_digits=15, decimal_places=2,
                                            null=True, blank=True)
    valuation_method = models.CharField(max_length=100, blank=True)
    previous_funding_rounds = models.TextField(blank=True)
    total_funding_raised = models.DecimalField(max_digits=15, decimal_places=2,
                                               null=True, blank=True)
    revenue_projections = models.TextField(blank=True)
    profit_projections = models.TextField(blank=True)
    market_size = models.DecimalField(max_digits=15, decimal_places=2,
                                      null=True, blank=True)
    market_growth_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                             null=True, blank=True)
    business_model = models.TextField(blank=True)
    revenue_streams = models.TextField(blank=True)
    user_acquisition_cost = models.DecimalField(max_digits=10,
                                                decimal_places=2, null=True,
                                                blank=True)
    customer_lifetime_value = models.DecimalField(max_digits=10,
                                                  decimal_places=2, null=True,
                                                  blank=True)
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                     blank=True)
    patents = models.TextField(blank=True)
    trademarks = models.TextField(blank=True)
    key_team_members = models.TextField(blank=True)
    advisors = models.TextField(blank=True)
    legal_structure = models.CharField(max_length=100, blank=True)
    regulatory_compliance = models.TextField(blank=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', null=True,
                                  blank=True)
    business_plan = models.FileField(upload_to='business_plans/', null=True,
                                     blank=True)
    financial_model = models.FileField(upload_to='financial_models/',
                                       null=True, blank=True)
    access_permissions = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    update_history = models.TextField(blank=True)

    def __str__(self):
        return f"DataRoom for {self.startup.username}"
