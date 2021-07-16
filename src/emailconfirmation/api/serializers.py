from rest_framework import serializers

from emailconfirmation.models import Emailconfirmation, Registerconfirmation

class EmailConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Emailconfirmation
        fields  = [
            'email',
            'name',
            'surname',
            'day',
            'month',
            'year',
            'time',
            'service',
            'shop'
        ]

class RegisterconfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Registerconfirmation
        fields = [
            'name',
            'surname',
            'email',
            'phone'
            ]
