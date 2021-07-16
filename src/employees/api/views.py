from rest_framework import generics
from .serializers import EmployeesSerializer
from rest_framework.response import Response
from employees.models import Employee
from rest_framework.response import Response
from store.models import Store
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class EmployeesAPIView(generics.ListAPIView):
    serializer_class = EmployeesSerializer

    def get_queryset(self):
        employee =self.request.GET['employee']
        empl_obj=Employee.objects.filter(employee=employee).first()
        shop = empl_obj.shop
        qs = Employee.objects.filter(shop=shop).all().order_by('id')
        return qs

class EmployeeDetailAPIView(generics.ListAPIView):
    serializer_class = EmployeesSerializer
    permission_classes  = [AllowAny]

    def get_queryset(self):
        shop =self.request.GET['shop']
        qs = Employee.objects.filter(shop=shop, display=True).all()
        return qs

class EmployeeDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = EmployeesSerializer
    queryset                = Employee.objects.all()