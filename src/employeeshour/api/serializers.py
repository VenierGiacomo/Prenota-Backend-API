from rest_framework import serializers

from employeeshour.models import Employeeshour

class EmploeehoursSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Employeeshour
        fields  =[
            'shop',
            'employee',
            'wkday',
            'start',
            'end',
            'start_t',
            'end_t',
        ]

