from rest_framework import serializers

from serviceaddons.models import ServiceAddOn

class ServiceAddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ServiceAddOn
        fields  =[
            'id',
            'service_id',
            'addon_id',
            'shop_id',

        ]
