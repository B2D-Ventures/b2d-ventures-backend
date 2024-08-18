from rest_framework import serializers
from b2d_ventures.app.models import Meeting
from .meeting_participant import MeetingParticipantSerializer


class MeetingSerializer(serializers.ModelSerializer):
    participants = MeetingParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ["id", "date", "status", "participants", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
