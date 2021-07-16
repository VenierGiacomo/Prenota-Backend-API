from rest_framework import serializers

from userdevices.models import UserDevice

class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = UserDevice
        fields  =[
            'id',
            'user',
            'player_id',
        ]