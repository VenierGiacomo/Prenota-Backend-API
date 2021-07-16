from rest_framework import serializers

from customservices.models import CustomService

class CustomServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CustomService
        fields  =[
            'id',
            'shop',
            'service',
            'store_client',
            'duration',
            'price'
        ]


