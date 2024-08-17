from rest_framework import serializers

from b2d_ventures.app.models import Startup
from b2d_ventures.app.serializers import UserSerializer


class StartupSerializer(UserSerializer):
    """
    Serializer for the Startup model.
    """

    class Meta(UserSerializer.Meta):
        model = Startup
        fields = UserSerializer.Meta.fields + [
            "name",
            "description",
            "fundraising_goal",
            "total_raised",
        ]

    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    fundraising_goal = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_raised = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True
    )
