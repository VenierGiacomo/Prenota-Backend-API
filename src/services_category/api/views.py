from rest_framework import generics
from services_category.models import ServiceCategory
from .serializers import ServiceCategorySerializer
from rest_framework.permissions import  AllowAny
from store.models import Store


class ServiceCategoryAPIView(generics.ListCreateAPIView):
        permission_classes  = [AllowAny]
        serializer_class = ServiceCategorySerializer

        def get_queryset(self,):
            shop = Store.objects.filter(id=self.request.GET['shop']).first()
            qs = ServiceCategory.objects.filter(shop=shop).all()
            return qs