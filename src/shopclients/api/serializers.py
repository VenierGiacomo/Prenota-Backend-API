from rest_framework import serializers

from shopclients.models import StoreClient

class StoreClientSerializer(serializers.ModelSerializer):
    class Meta:
        model   = StoreClient
        fields  =[
            'id',
            'shop',
            'client_name',
            'client',
            'phone',
            'email',
            'credit',
            'note',
            'isMember',
        ]


