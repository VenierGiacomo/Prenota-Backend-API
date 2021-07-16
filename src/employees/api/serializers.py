from rest_framework import serializers

from employees.models import Employee

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Employee
        fields  =[
            'id',
            'shop',
            'employee',
            'name',
        ]