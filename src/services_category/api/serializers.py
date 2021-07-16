from rest_framework import serializers

from services_category.models import ServiceCategory

class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model   = ServiceCategory
        fields  =[
            'id',
            'name',
            'shop',
        ]


