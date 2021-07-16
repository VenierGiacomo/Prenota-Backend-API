from rest_framework import generics
from addons.models import AddOn
from .serializers import AddOnSerializer
from rest_framework.permissions import  AllowAny



class AddonsAPIView(generics.ListCreateAPIView):
        permission_classes  = [AllowAny]
        serializer_class = AddOnSerializer
        queryset        = AddOn.objects.all()