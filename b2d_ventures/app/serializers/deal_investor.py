from rest_framework import serializers

from b2d_ventures.app.models import DealInvestor
from .deal import DealSerializer
from .user import UserSerializer


class DealInvestorSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only=True)
    investor = UserSerializer(read_only=True)

    class Meta:
        model = DealInvestor
        fields = ['id', 'deal', 'investor', 'investment_amount',
                  'investment_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'investment_date', 'created_at',
                            'updated_at']
