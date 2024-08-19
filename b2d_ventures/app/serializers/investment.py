from rest_framework import serializers

from b2d_ventures.app.models import Investment


class InvestmentSerializer(serializers.ModelSerializer):
    investor = serializers.StringRelatedField()
    deal = serializers.StringRelatedField()

    class Meta:
        model = Investment
        fields = [
            "id",
            "investor",
            "deal",
            "amount",
            "date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "date",
            "created_at",
            "updated_at",
        ]
