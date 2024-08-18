from rest_framework import serializers
from b2d_ventures.app.models import Deal
from b2d_ventures.app.serializers import StartupSerializer


class DealSerializer(serializers.ModelSerializer):
    startup = StartupSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'startup', 'name', 'content', 'image_url',
                  'allocation',
                  'price_per_unit', 'minimum_investment', 'raised',
                  'start_date',
                  'end_date', 'investor_count', 'status', 'created_at',
                  'updated_at']
        read_only_fields = ['id', 'raised', 'investor_count', 'created_at',
                            'updated_at']
