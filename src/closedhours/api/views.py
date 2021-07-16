from rest_framework import generics
from closedhours.models import Closedhours
from .serializers import ClosedhoursSerializer
from rest_framework.response import Response
from store.models import Store
from rest_framework import status

class ClosedhoursAPIView(generics.ListCreateAPIView):
    queryset         = Closedhours.objects.all()
    serializer_class = ClosedhoursSerializer

    def get_queryset(self,):
        shop_id=Store.objects.filter(owner=self.request.user).first()
        qs = Closedhours.objects.filter(shop=shop_id).all()
        return qs

    def post(self, request, format=None):
        work_hours=request.data
        shop_id = Store.objects.filter(owner=self.request.user).first().id
        Closedhours.objects.filter(shop=shop_id).delete()
        for day_hours in  work_hours:
            day_hours['shop']=shop_id
            serializer = ClosedhoursSerializer(data=day_hours)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClosedhoursDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Closedhours.objects.all()
    serializer_class = ClosedhoursSerializer