from rest_framework import serializers

from b2d_ventures.app.models import DataRoom


class DataRoomSerializer(serializers.ModelSerializer):
    startup = serializers.StringRelatedField()
    data_room_pdf = serializers.FileField(required=False)

    class Meta:
        model = DataRoom
        fields = ['id', 'startup', 'data_room_pdf', 'access_permissions',
                  'last_updated']
        read_only_fields = ('startup', 'last_updated')
