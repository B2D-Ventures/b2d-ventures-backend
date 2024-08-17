from rest_framework import serializers

from b2d_ventures.app.models import Admin
from b2d_ventures.app.serializers import UserSerializer


class AdminSerializer(UserSerializer):
    """
    Serializer for the Admin model.
    """

    permission = serializers.CharField()

    class Meta(UserSerializer.Meta):
        model = Admin
