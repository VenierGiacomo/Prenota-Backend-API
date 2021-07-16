from rest_framework import generics
from customservices.models import CustomService
from store.models import Store
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomServiceSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication



class CustomServicesAPIView(generics.ListCreateAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        serializer_class        = CustomServiceSerializer
        queryset                = CustomService.objects.all()

        def post(self, request, format=None):
            data=request.data
            if CustomService.objects.filter(store_client=data['store_client'],service=data['service']).first() == None:
                store = Store.objects.filter(owner=self.request.user).first()
                if store != None:
                    data['shop'] = store.id
                    serializer = CustomServiceSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'exist':True}, status=status.HTTP_400_BAD_REQUEST)

        def list(self, request, *args, **kwargs):
            client_id = request.GET['client_id']
            shop = Store.objects.filter(owner=self.request.user).first()
            if shop != None:
                queryset =CustomService.objects.filter(shop=shop, store_client=client_id).all()
                serializer = CustomServiceSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomServicesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        serializer_class        = CustomServiceSerializer
        queryset                = CustomService.objects.all()

        def update(self, request, pk,*kwarg):
            shop = Store.objects.filter(owner=self.request.user).first()
            if shop != None:
               data=request.data
               if CustomService.objects.filter(id=pk,shop=shop).first() != None:
                  CustomService.objects.filter(id=pk).update(price=data['price'],duration=data['duration'])
                  qs = CustomService.objects.filter(id=pk).first()
                  ser = CustomServiceSerializer(qs,many=False)
                  return Response(ser.data)
            return Response({'owner':False}, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            shop = Store.objects.filter(owner=self.request.user).first()
            if shop != None:
                qs= CustomService.objects.filter(id=pk,shop=shop).first()
                qs.delete()
                return Response({'message': "Cancellato"}, status=203)
            return Response({'owner':False}, status=status.HTTP_400_BAD_REQUEST)




