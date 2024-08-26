from rest_framework import serializers

from b2d_ventures.app.models import Deal
from b2d_ventures.app.serializers import StartupSerializer


class DealSerializer(serializers.ModelSerializer):
    startup = StartupSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = [
            "id",
            "startup",
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
        ]
        read_only_fields = [
            "id",
            "raised",
            "investor_count",
        ]
