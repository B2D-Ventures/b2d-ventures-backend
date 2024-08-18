from rest_framework import serializers
from b2d_ventures.app.models import MeetingParticipant
from b2d_ventures.app.serializers import InvestorSerializer, StartupSerializer


class MeetingParticipantSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer(read_only=True)
    startup = StartupSerializer(read_only=True)

    class Meta:
        model = MeetingParticipant
        fields = ["id", "meeting", "investor", "startup", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
