from rest_framework import serializers

from employeeservices.models import EmployeeServices

class EmployeeServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = EmployeeServices
        fields  =[
            'id',
            'shop',
            'employee',
            'service_id'
        ]
