from rest_framework import serializers

from webhooks.models import StripeData

class StripeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model   = StripeData
        fields  =[
            'id',
            'hook_type',
            'data_string',
            'client',
        ]