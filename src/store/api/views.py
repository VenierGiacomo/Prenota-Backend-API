from rest_framework import generics
from store.models import Store
from employees.models import Employee
from .serializers import StoreSerializer, UpdateStoreSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

User = get_user_model()

class StoreAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = Store.objects.all()
    serializer_class        = StoreSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def post(self, request, format=None):
        data=request.data
        data['owner'] = self.request.user.id
        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            employee_id = self.request.user
            Employee.objects.create(shop=instance, employee=employee_id, name=self.request.user.first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreListAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    queryset                = Store.objects.filter(display=True).all().order_by('order_priority')
    serializer_class        = StoreSerializer

class StoreList1APIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    queryset                = Store.objects.filter(display_1=True).all().order_by('order_priority')
    serializer_class        = StoreSerializer


class HasStoreListAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    queryset                = Store.objects.all()
    serializer_class        = StoreSerializer

    def get(self, request, format=None):
        store = Store.objects.filter(owner=self.request.user.id).first()
        print(store, 'afff')
        # store.has_store =True
        if store is None:
            return Response({'has_store':False})
        else:
            serializer = StoreSerializer(store)
            return Response(serializer.data)
            # return Response({'has_store':False})
            # return Response(store)

class StoreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Store.objects.all()
    serializer_class = UpdateStoreSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    lookup_url_kwarg        = "owner"

    def get_object(self):
        owner =self.kwargs.get(self.lookup_url_kwarg)
        qs =Store.objects.filter(owner=owner).first()
        return qs

# class StoreDetailIdAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset         = Store.objects.all()
#     serializer_class = StoreSerializer
#     permission_classes      = [AllowAny]



class StoreDetailIdAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes      = [AllowAny]

    lookup_url_kwarg        = "id"

    def get_object(self):
        id =self.kwargs.get(self.lookup_url_kwarg)
        qs =Store.objects.filter(id=id).first()
        return qs


class StoresCategoryAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    # queryset                = Store.objects.filter(display=True).all().order_by('business_type')
    serializer_class        = StoreSerializer
    lookup_url_kwarg        = "category"

    def get_queryset(self):
        category =self.kwargs.get(self.lookup_url_kwarg)
        qs =Store.objects.filter(business_type=category,display=True).all()
        print(qs, category)
        return qs

    # def get_queryset(self):
    #     owner =self.kwargs.get(self.lookup_url_kwarg)
    #     qs =Store.objects.filter(owner=owner).first()
    #     print('dio can',owner, qs)
    #     return qs

    # def update(self, instance, validated_data):
    #     print(instance,validated_data)
    #     return {}


