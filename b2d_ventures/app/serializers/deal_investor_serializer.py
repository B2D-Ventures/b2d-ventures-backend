from rest_framework import serializers

from b2d_ventures.app.models import DealInvestor
from .deal_serializer import DealSerializer
from .user_serializer import UserSerializer


class DealInvestorSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only=True)
    investor = UserSerializer(read_only=True)

    class Meta:
        model = DealInvestor
        fields = ['id', 'deal', 'investor', 'investment_amount',
                  'investment_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'investment_date', 'created_at',
                            'updated_at']

    def create(self, validated_data):
        investor = self.context['request'].user
        deal = self.context['deal']
        return DealInvestor.objects.create(investor=investor, deal=deal,
                                           **validated_data)

    def validate_investment_amount(self, value):
        deal = self.context['deal']
        if value < deal.minimum_investment:
            raise serializers.ValidationError(
                f"Investment amount must be at least {deal.minimum_investment}")
        return value

    def validate(self, data):
        deal = self.context['deal']
        investor = self.context['request'].user
        if DealInvestor.objects.filter(deal=deal, investor=investor).exists():
            raise serializers.ValidationError(
                "You have already invested in this deal")
        return data
