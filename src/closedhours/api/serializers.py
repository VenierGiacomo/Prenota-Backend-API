from rest_framework import serializers

from closedhours.models import Closedhours

class ClosedhoursSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Closedhours
        fields  =[
            'shop',
            'wkday',
            'start',
            'end',
        ]
      
