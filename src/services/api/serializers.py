from rest_framework import serializers

from services.models import ServicesStore

class ServicesStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ServicesStore
        fields  =[
            'id',
            'shop',
            'name',
            'duration',
            'duration_book',
            'sex',
            'max_n',
            'price',
            'color',
            'category',
            'favorite',
            'hasToBeMember',
            'hasToBeCLient',
        ]
