from rest_framework import serializers
from b2d_ventures.app.models import Investor
from b2d_ventures.app.serializers import UserSerializer


class InvestorSerializer(UserSerializer):
    """
    Serializer for the Investor model.
    """

    available_funds = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_invested = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True
    )

    class Meta(UserSerializer.Meta):
        model = Investor
