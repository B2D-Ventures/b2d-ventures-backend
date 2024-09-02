from rest_framework import serializers

from b2d_ventures.app.models import Meeting, Investor, Startup
from b2d_ventures.app.serializers import InvestorSerializer, StartupSerializer


class MeetingSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer(read_only=True)
    investor_id = serializers.PrimaryKeyRelatedField(
        queryset=Investor.objects.all(), source="investor", write_only=True
    )
    startup = StartupSerializer(read_only=True)
    startup_id = serializers.PrimaryKeyRelatedField(
        queryset=Startup.objects.all(), source="startup", write_only=True
    )

    class Meta:
        model = Meeting
        fields = [
            "id",
            "date",
            "investor",
            "investor_id",
            "startup",
            "startup_id",
            "status",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Meeting.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
