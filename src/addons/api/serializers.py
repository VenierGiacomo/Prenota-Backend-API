from rest_framework import serializers

from addons.models import AddOn

class AddOnSerializer(serializers.ModelSerializer):

    class Meta:
        model   = AddOn
        fields  =[
            'id',
            'id_c',
            'name',
            'shop',
            'price',
            'duration',
            'description',

        ]


