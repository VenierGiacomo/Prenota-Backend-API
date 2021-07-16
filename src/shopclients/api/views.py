from rest_framework import generics
from rest_framework.response import Response
from shopclients.models import StoreClient
from store.models import Store
from .serializers import StoreClientSerializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
import pusher
from bookings.models import Bookings

class StoreClientsAPIView(generics.ListCreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer

    def get_queryset(self):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = StoreClient.objects.filter(shop=own_shop).all().order_by('-id')
        return qs

    def perform_create(self, serializer):

        if 'shop' in self.request.data:
            shop=self.request.data['shop']
        else:
            shop = Store.objects.filter(owner=self.request.user).first()
        serializer.save(shop=shop)
        User = get_user_model()
        if 'client_id' in self.request.data:
            if StoreClient.objects.filter(shop=shop, client=self.request.data['client_id']).first()== None:
                client = User.objects.filter(id=self.request.data['client_id']).first()
                phone = client.phone
                email = client.email
                client_name = client.first_name + ' ' + client.last_name
                serializer.save(note='')



            else:

                return Response({'account': 'already exists'}, status=200)
        else:
            client_name=self.request.data['client_name']
            client = User.objects.filter(id=1).first()
            email= self.request.data['email']
            phone=self.request.data['phone']
        serializer.save(email=email)
        serializer.save(phone=phone)
        serializer.save(client=client)
        serializer.save(shop=shop)
        serializer.save(client_name=client_name)

class StoreClientsByQRCodeAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer


    def perform_create(self, serializer):
        StoreClient.objects.filter(id=self.request.data['id']).update(client=self.request.user)
        pusher_client = pusher.Pusher(
          app_id='1161409',
          key='45f982633227395f42a9',
          secret='539affddd1466113919b',
          cluster='eu',
          ssl=True
        )
        customer_obj = StoreClient.objects.filter(id=self.request.data['id']).first()
        shop_name = customer_obj.shop.store_name
        channel_name = shop_name.replace(' ','-')

        pusher_client.trigger(channel_name, 'update-costumer', {'client_id': self.request.data['id'], 'id': self.request.user.id})
        Bookings.objects.filter(store_client=self.request.data['id']).update(client=self.request.user)



class StoreClientsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer
    queryset                = StoreClient.objects.all()


class IsStoreClientsAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer

    def get_queryset(self):
        shop = self.request.GET['shop']
        client = self.request.user.id
        qs = StoreClient.objects.filter(shop=shop, client=client)
        return qs

class StoreClientsNewAPIView(generics.ListCreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer

    def get_queryset(self):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = StoreClient.objects.filter(shop=own_shop).all()
        return qs

    def perform_create(self, serializer):
        shop = Store.objects.filter(owner=self.request.user).first()
        User = get_user_model()
        # # send_mail( subject, message, email_from, recipient_list, html_message=html_message  )
        client_name = self.request.data['first_name'] + ' ' + self.request.data['last_name']
        client = User.objects.filter(id=1).first()
        if 'email' in self.request.data:
            serializer.save(phone=self.request.data['phone'], email=self.request.data['email'], client=client, shop=shop, client_name=client_name)
        else:
            serializer.save(phone=self.request.data['phone'], client=client, shop=shop, client_name=client_name)
        # if 'email' in self.request.data:
        #     email_from = settings.EMAIL_HOST_USER
        #     url_shop = shop.store_name.replace(' ', '%20')
        #     # html_message = render_to_string('email_template_no_address.html',{'surname': data['surname'], 'name': data['name'], 'day':data['day'], 'month': data['month'], 'year': data['year'], 'shop': data['shop'], 'time':data['time'], 'address':''})
        #     subject =  shop.store_name + ' - Finalmente ci può prenotare online'
        #     message = 'Salve, sono ' + shop.owner_name + ', ci tenevo ad informarla che '+shop.store_name + " è finalmente prenotabile online!\n\nPuò scaricare l'app da questo link: https://prenota.cc/app\n\nPer semplificare al massimo la sua esperienza, le abbiamo già creato un account! Quando ha scaricato l'app, clicchi qui sotto:\nhttps://prenota.cc/register/"+ self.request.data['first_name'] + '/' + self.request.data['last_name'] +'/'+ self.request.data['email']+'/'+ self.request.data['phone'] +'/'+url_shop+'/'+str(obj.id)+'\n\nPer qualsiasi dubbio o difficoltà, restiamo a sua disposizione!\n\nCordiali saluti,\n'+shop.store_name + " Team Prenota"
        #     recipient_list = [self.request.data['email']]
        #     send_mail( subject, message, email_from, recipient_list)
        # serializer.save(client=client)
        # serializer.save(shop=shop)
        # serializer.save(client_name=client_name)

class StoreClientsInviteEmailAPIView(generics.ListCreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StoreClientSerializer

    def get_queryset(self):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = StoreClient.objects.filter(shop=own_shop).all()
        return qs

    def perform_create(self, serializer):
        shop = Store.objects.filter(owner=self.request.user).first()
        client = StoreClient.objects.filter(shop=shop, id=self.request.data['id']).first()
        client.first_name = client.client_name.split()[0]
        client.last_name = client.client_name.split()[1]
        email_from = shop.store_name + ' <'+ settings.EMAIL_HOST_USER+ '>'
        url_shop = shop.store_name.replace(' ', '%20')
        # html_message = render_to_string('email_template_no_address.html',{'surname': data['surname'], 'name': data['name'], 'day':data['day'], 'month': data['month'], 'year': data['year'], 'shop': data['shop'], 'time':data['time'], 'address':''})
        subject =  shop.store_name + ' - Finalmente ci può prenotare online'
        message = 'Salve, sono ' + shop.owner_name + ', ci tenevo ad informarla che '+shop.store_name + " è finalmente prenotabile online!\n\nPuò scaricare l'app da questo link: https://prenota.cc/app\n\nPer semplificare al massimo la sua esperienza, le abbiamo già creato un account! Quando ha scaricato l'app, clicchi qui sotto:\nhttps://prenota.cc/register/"+ client.first_name + '/' + client.last_name +'/'+ client.email+'/'+ client.phone+'/'+url_shop+'/'+str(client.id)+'\n\nPer qualsiasi dubbio o difficoltà, restiamo a sua disposizione!\n\nCordiali saluti,\n'+shop.store_name + " Team Prenota"
        recipient_list = [client.email]
        send_mail( subject, message, email_from, recipient_list)