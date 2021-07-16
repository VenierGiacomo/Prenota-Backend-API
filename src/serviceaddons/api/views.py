from rest_framework import generics
from addons.models import AddOn
from serviceaddons.models import ServiceAddOn
from addons.api.serializers import AddOnSerializer
from .serializers import ServiceAddOnSerializer
from store.models import Store
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


class ServiceAddOnsAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    serializer_class        = AddOnSerializer
    lookup_url_kwarg        = "service_id"

    def get_queryset(self,):
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = ServiceAddOn.objects.filter(service_id=service_id).all()
        return qs

    def get(self, request, service_id,format=None):
        queryset = ServiceAddOnsAPIView.get_queryset(self)
        Adons = []
        for adon_obj in queryset:
            Adons.append(adon_obj.addon_id.__dict__)
        serailized_adon = AddOnSerializer(data=Adons, many=True)
        if serailized_adon.is_valid():
            print(serailized_adon.__dict__)
            return Response(serailized_adon.data, status=200)
        return Response(serailized_adon.errors, status=200)

class StoreAddOnsAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = ServiceAddOnSerializer

    def get_queryset(self,):
        shop = Store.objects.filter(owner=self.request.user).first()
        qs = ServiceAddOn.objects.filter(shop_id=shop).all()
        return qs


