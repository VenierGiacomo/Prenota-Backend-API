from rest_framework import generics
from .serializers import UserDeviceSerializer
from rest_framework.response import Response
from userdevices.models import UserDevice
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class DeviceAPIView(generics.CreateAPIView):
    serializer_class = UserDeviceSerializer
    quesyset         = UserDevice.objects.all()
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]

    def perform_create(self, serializer):
        dev =  UserDevice.objects.filter(player_id=self.request.data['player_id']).first()
        if  dev == None:
            serializer.save()
        else:
           dev.delete()
           serializer.save()