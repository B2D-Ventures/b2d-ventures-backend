from django.core.exceptions import ValidationError
from rest_framework import serializers

from b2d_ventures.app.models import Deal, Startup
from b2d_ventures.app.serializers import StartupSerializer


class DealSerializer(serializers.ModelSerializer):
    startup = StartupSerializer(read_only=True)
    startup_id = serializers.PrimaryKeyRelatedField(
        queryset=Startup.objects.all(), source="startup", write_only=True
    )
    dataroom_url = serializers.SerializerMethodField()
    image_background_url = serializers.SerializerMethodField()
    image_logo_url = serializers.SerializerMethodField()
    image_content_url = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = [
            "id",
            "startup",
            "startup_id",
            "name",
            "description",
            "content",
            "image_background",
            "image_background_url",
            "image_logo",
            "image_logo_url",
            "image_content",
            "image_content_url",
            "target_amount",
            "price_per_unit",
            "minimum_investment",
            "type",
            "amount_raised",
            "start_date",
            "end_date",
            "investor_count",
            "status",
            "dataroom",
            "dataroom_url",
        ]
        read_only_fields = [
            "id",
            "investor_count",
            "dataroom_url",
            "image_background_url",
            "image_logo_url",
            "image_content_url",
        ]

    def get_dataroom_url(self, obj):
        if obj.dataroom:
            return obj.dataroom.url
        return None

    def get_image_background_url(self, obj):
        if obj.image_background:
            return obj.image_background.url
        return None

    def get_image_logo_url(self, obj):
        if obj.image_logo:
            return obj.image_logo.url
        return None

    def get_image_content_url(self, obj):
        if obj.image_content:
            return obj.image_content.url
        return None

    def validate_dataroom(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:  # 10 MB
                raise ValidationError("File size cannot exceed 10 MB.")
        return value

    def validate_image_field(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError("Image size cannot exceed 5 MB.")
        return value

    def validate_image_background(self, value):
        return self.validate_image_field(value)

    def validate_image_logo(self, value):
        return self.validate_image_field(value)

    def validate_image_content(self, value):
        return self.validate_image_field(value)

    def create(self, validated_data):
        return Deal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
