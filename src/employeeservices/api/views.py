from rest_framework import generics
from .serializers import EmployeeServicesSerializer
from rest_framework.response import Response
from employeeservices.models import EmployeeServices
from store.models import Store
from rest_framework import status

class EmployeeServicesAPIView(generics.ListCreateAPIView):
    queryset         = EmployeeServices.objects.all()
    serializer_class = EmployeeServicesSerializer

    def post(self, request, format=None):
            data=request.data
            store = Store.objects.filter(owner=self.request.user).first()
            data['shop'] = store.id
            serializer = EmployeeServicesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        owner = request.GET['owner']
        store = Store.objects.filter(owner=owner).first()
        queryset =EmployeeServices.objects.filter(shop=store)
        serializer = EmployeeServicesSerializer(queryset, many=True)
        return Response(serializer.data)

class EmployeeServicesfromStoreAPIView(generics.ListAPIView):
    queryset         = EmployeeServices.objects.all()
    serializer_class = EmployeeServicesSerializer

    def list(self, request, *args, **kwargs):
        store_id = request.GET['store']
        queryset =EmployeeServices.objects.filter(shop=store_id)
        serializer = EmployeeServicesSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeServicesdetatilAPIView(generics.DestroyAPIView):
    queryset         = EmployeeServices.objects.all()
    serializer_class = EmployeeServicesSerializer

    # def get_object(self):

    def delete(self, request, *args, **kwargs):
        employee = self.kwargs.get('employee')
        service = self.kwargs.get('service')
        list_services = EmployeeServices.objects.filter(employee=employee, service_id=service).all()
        list_services.delete()
        # print(employee, service, list_services)
        return Response(status=status.HTTP_200_OK)
    # def post(self, request, format=None):
    #         data=request.data
    #         store = Store.objects.filter(owner=self.request.user).first()
    #         data['shop'] = store.id
    #         serializer = EmployeeServicesSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
