from rest_framework import generics
from .serializers import ServicesStoreSerializer
from rest_framework.response import Response
from services.models import ServicesStore
from store.models import Store
from rest_framework import status
from rest_framework.permissions import AllowAny

class ServicesStoreAPIView(generics.ListCreateAPIView):
    queryset         = ServicesStore.objects.all()
    serializer_class = ServicesStoreSerializer
    permission_classes  = [AllowAny]

    def post(self, request, format=None):
            data=request.data
            store = Store.objects.filter(owner=self.request.user).first()
            data['shop'] = store.id
            serializer = ServicesStoreSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        owner = request.GET['owner']
        store = Store.objects.filter(owner=owner).first()
        queryset =ServicesStore.objects.filter(shop=store)
        serializer = ServicesStoreSerializer(queryset, many=True)
        return Response(serializer.data)

class ServicesStoreByShopAPIView(generics.ListAPIView):
    queryset         = ServicesStore.objects.all()
    serializer_class = ServicesStoreSerializer
    permission_classes  = [AllowAny]

    def list(self, request, *args, **kwargs):
        shop = request.GET['shop']
        queryset =ServicesStore.objects.filter(shop=shop, display=True).all()
        serializer = ServicesStoreSerializer(queryset, many=True)
        return Response(serializer.data)

class ServicesStoreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServicesStoreSerializer

    def get_queryset(self):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = ServicesStore.objects.filter(shop=own_shop).all()
        return qs

# class ServicesStoreDefaultAllAPIView(generics.ListCreateAPIView):
#     serializer_class = ServicesStoreSerializer
#     # qs = ServicesStore.objects.all()

#     def get_queryset(self):
#         qs = ServicesStore.objects.all()
#         for serv in qs:
#             serv.duration_book =serv.duration
#             serv.save()
#         # qs[0].duration_book =qs[0].duration
#         # qs[0].save()
#         return qs