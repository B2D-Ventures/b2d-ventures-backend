from django.core.exceptions import ValidationError
from rest_framework import serializers

from b2d_ventures.app.models import Deal, Startup
from b2d_ventures.app.serializers import StartupSerializer


class DealSerializer(serializers.ModelSerializer):
    startup = StartupSerializer(read_only=True)
    startup_id = serializers.PrimaryKeyRelatedField(
        queryset=Startup.objects.all(),
        source='startup',
        write_only=True
    )
    dataroom_url = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = [
            "id",
            "startup",
            "startup_id",
            "name",
            "content",
            "image_background_url",
            "image_logo_url",
            "image_content_url",
            "allocation",
            "price_per_unit",
            "minimum_investment",
            "type",
            "raised",
            "start_date",
            "end_date",
            "investor_count",
            "status",
            "dataroom_url",
        ]
        read_only_fields = [
            "id",
            "raised",
            "investor_count",
            "dataroom_url",
        ]

    def get_dataroom_url(self, obj):
        if obj.dataroom:
            return obj.dataroom.url
        return None

    def validate_dataroom(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 10 MB.")
        return value

    def create(self, validated_data):
        dataroom = validated_data.pop('dataroom', None)
        instance = super().create(validated_data)
        if dataroom:
            instance.dataroom = dataroom
            instance.save()
        return instance

    def update(self, instance, validated_data):
        dataroom = validated_data.pop('dataroom', None)
        instance = super().update(instance, validated_data)
        if dataroom:
            instance.dataroom = dataroom
            instance.save()
        return instance
