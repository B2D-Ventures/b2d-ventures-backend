from rest_framework import serializers

from b2d_ventures.app.models import Admin
from b2d_ventures.app.serializers import UserSerializer


class AdminSerializer(UserSerializer):
    """
    Serializer for the Admin model.
    """

    class Meta(UserSerializer.Meta):
        model = Admin
        fields = UserSerializer.Meta.fields + ["permission"]

    permission = serializers.CharField()
