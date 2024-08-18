from rest_framework import serializers

from b2d_ventures.app.models import DataRoom


class DataRoomSerializer(serializers.ModelSerializer):
    startup = serializers.StringRelatedField()
    pitch_deck = serializers.FileField(required=False)
    business_plan = serializers.FileField(required=False)
    financial_model = serializers.FileField(required=False)

    class Meta:
        model = DataRoom
        fields = "__all__"
        read_only_fields = ("startup", "last_updated")
