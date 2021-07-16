from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from bookings.models import Bookings
from store.models import Store
from userdevices.models import UserDevice
from shopclients.models import StoreClient
from customservices.models import CustomService
from .serializers import BookingsSerializer, BookingsLightSerializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime
from services.models import ServicesStore
from datetime import timedelta
import json
import requests
from django.core.mail import send_mail
from django.conf import settings
from addons.models import AddOn
from shopclients.models import StoreClient
times =["06:00", "06:05", "06:10", "06:15", "06:20", "06:25", "06:30", "06:35", "06:40","06:45", "06:50", "06:55", "07:00", "07:05", "07:10", "07:15", "07:20", "07:25", "07:30", "07:35", "07:40", "07:45", "07:50", "07:55", "08:00", "08:05", "08:10", "08:15", "08:20", "08:25", "08:30", "08:35", "08:40", "08:45", "08:50", "08:55", "09:00", "09:05", "09:10", "09:15", "09:20", "09:25", "09:30", "09:35", "09:40", "09:45", "09:50", "09:55", "10:00", "10:05", "10:10", "10:15", "10:20", "10:25", "10:30", "10:35", "10:40", "10:45", "10:50", "10:55", "11:00", "11:05", "11:10", "11:15", "11:20", "11:25", "11:30", "11:35", "11:40", "11:45", "11:50", "11:55", "12:00", "12:05", "12:10", "12:15", "12:20", "12:25", "12:30", "12:35", "12:40", "12:45", "12:50", "12:55", "13:00", "13:05", "13:10", "13:15", "13:20", "13:25", "13:30", "13:35", "13:40", "13:45", "13:50", "13:55","14:00", "14:05", "14:10", "14:15", "14:20", "14:25", "14:30", "14:35", "14:40", "14:45", "14:50", "14:55", "15:00", "15:05", "15:10", "15:15", "15:20", "15:25", "15:30", "15:35", "15:40", "15:45", "15:50", "15:55", "16:00", "16:05", "16:10", "16:15", "16:20", "16:25", "16:30", "16:35", "16:40", "16:45", "16:50", "16:55", "17:00", "17:05", "17:10", "17:15", "17:20", "17:25", "17:30", "17:35", "17:40", "17:45", "17:50", "17:55", "18:00", "18:05", "18:10", "18:15", "18:20", "18:25", "18:30", "18:35", "18:40", "18:45", "18:50", "18:55", "19:00", "19:05", "19:10", "19:15", "19:20", "19:25", "19:30", "19:35", "19:40", "19:45", "19:50", "19:55", "20:00", "20:05", "20:10", "20:15", "20:20", "20:25", "20:30", "20:35", "20:40", "20:45", "20:50", "20:55", "21:00", "21:05", "21:10", "21:15", "21:20", "21:25", "21:30", "21:35", "21:40", "21:45", "21:50", "21:55", "22:00", "22:05", "22:10", "22:15","22:20", "22:25", "22:30", "22:35", "22:40", "22:45", "22:50", "22:55", "23:00", "23:05", "23:10", "23:15", "23:20", "23:25", "23:30", "23:35", "23:40", "23:45", "23:50", "23:55" ]
rows = ["06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "20:45", "21:00", "21:15", "21:30", "21:45", "22:00", "22:15", "22:30", "22:45", "23:00", "23:15", "23:30", "23:45", "24:00"]
months=['Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']


class BookingsAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class = BookingsSerializer

    def get_queryset(self):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = Bookings.objects.filter(shop=own_shop).all()
        return qs

    def perform_create(self, serializer):
        details = self.request.data['details']
        if 'new' in self.request.data:
            start_t = self.request.data['start']
            end_t = self.request.data['end']
            start = (start_t-9)/3
            end = start + (end_t - start_t)
            cont =  self.request.data['client_name']+" " + self.request.data['details'] +  " il " +str(self.request.data['day'])+ " "  + months[self.request.data['month']] + " alle " + times[start_t]
        else:
            start = self.request.data['start']
            end = self.request.data['end']
            start_t = times.index(rows[self.request.data['start']])
            end_t = start_t+ self.request.data['end'] - self.request.data['start']
            cont =  self.request.data['client_name']+" " + self.request.data['details'] +  " il " +str(self.request.data['day'])+ " "  + months[self.request.data['month']] + " alle " + rows[start]


        if Bookings.objects.filter( employee=self.request.data['employee'], day=self.request.data['day'], month=self.request.data['month'], year=self.request.data['year'], start_t__lt=end_t,end_t__gt=start_t).first() == None:
            if int(self.request.data['service_n'])>0 :
                service_id = self.request.data['service_n']
                service = ServicesStore.objects.filter(id=service_id).first()
                if self.request.data['month'] >4 and self.request.data['month'] < 9:
                    price = service.price_2
                else:
                    price = service.price

                if 'adons' in self.request.data :
                    adons_list = self.request.data['adons']
                    for adon_id in adons_list:
                        adon = AddOn.objects.filter(id=adon_id).first()
                        details = details + ' + ' + adon.name

                        end = end + adon.duration
                        end_t = end_t + adon.duration

                        price= price + adon.price
                serializer.save(price=price)

            if 'shop' in self.request.data:
                if StoreClient.objects.filter(shop=self.request.data['shop'], client=self.request.user).first() == None:
                    if self.request.data['employee'] != self.request.user:
                        shop = Store.objects.filter(id=self.request.data['shop']).first()
                        StoreClient.objects.create(shop=shop, client_name=self.request.data['client_name'], client=self.request.user, phone=self.request.data['phone'], note='Ultimo servizio: '+self.request.data['details'],)
              
                shop = Store.objects.filter(id=self.request.data['shop']).first()

                header = {"Content-Type": "application/json; charset=utf-8",
                        
                        }
                devices = UserDevice.objects.filter(user=shop.owner)
                ids=[]
                serializer.save(store_phone=shop.phone_number,store_name=shop.store_name,location=shop.address, shop=shop,client=self.request.user,day_to_delete=shop.cancel_advance)
                for device in devices:
                    ids.append(device.player_id)
                ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
                ids.append('a416d507-a073-4ec5-983b-cd6dff542160')
                ids.append('2be8c721-b0af-4dbd-8502-2647e754f61e')

                not_data ={"day":self.request.data['day'],"month":self.request.data['month'],"year":self.request.data['year'],"start":start_t,"employee":self.request.data['employee']}
                title = shop.store_name +": Nuova prenotazione 🙂"
               
                payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "data": not_data,
                        "contents": {"en": cont}}
                requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

                serializer.save(details=details,start=start,end=end, start_t=start_t, end_t=end_t,booked_on_plt=True)

            else:
                if Store.objects.filter(owner=self.request.user).first() == None:
                    raise serializers.ValidationError({'message': "You need to be specify a shop"})
                    raise Response({'message': "You need to be specify a shop"}, status=400)
                    # print('no shop')
                else:
                    shop = Store.objects.filter(owner=self.request.user).first()
                    User = get_user_model()
                    if 'client' in self.request.data and self.request.data['client']>1:
                         client = User.objects.filter(id=self.request.data['client']).first()
                         store_client = StoreClient.objects.filter(client=client, shop=shop).first()
                         if store_client != None:
                            serializer.save(store_client=store_client.id)
                    else:
                        client = User.objects.filter(id=1).first()
                        if 'store_client' in self.request.data:
                            serializer.save(store_client=self.request.data['store_client'])
                            store_client = StoreClient.objects.filter(id=self.request.data['store_client']).first()
                            if store_client != None and store_client.client.id >1 :
                                client = User.objects.filter(id=store_client.client.id).first()


                    header = {"Content-Type": "application/json; charset=utf-8",
                            
                            }
                    ids=[]
                    if shop.id>50:
                        if client.id != 1 :
                            devices = UserDevice.objects.filter(user=client.id).all()
                            ids=[]
                            for device in devices:
                                ids.append(device.player_id)
                            splitted_time = times[start_t].split(':')
                            date_of_appo = datetime.datetime(self.request.data['year'],self.request.data['month']+1,self.request.data['day'],int(splitted_time[0])-2,int(splitted_time[1]),0)
                            date_before = datetime.datetime(self.request.data['year'],self.request.data['month']+1,self.request.data['day'],11,0,0) - timedelta(days=1)
                            title = "Buongiorno, hai un appuntamento domani"
                            cont =   "Ricorrdati il tuo appuntamento domani alle " + times[start_t] +" presso " + shop.store_name
                            payload = {"app_id": "91f9f284-1a50-44c4-8d5d-7ff9102e75a0",
                                    "include_player_ids":ids ,
                                    "headings": {"en": title},
                                    "send_after": date_before.strftime("%Y-%m-%d %H:%M:%S")+" GMT+0200",
                                    "contents": {"en": cont}}
                            requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                            title = "Mancano 2 ore!"
                            cont =   "Ricordati del tuo appuntamento oggi alle " + times[start_t] +" presso " + shop.store_name
                            payload = {"app_id": "91f9f284-1a50-44c4-8d5d-7ff9102e75a0",
                                    "include_player_ids":ids ,
                                    "headings": {"en": title},
                                    "send_after": date_of_appo.strftime("%Y-%m-%d %H:%M:%S")+" GMT+0200",
                                    "contents": {"en": cont}}
                            requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                        ids.append('e3a3c2d4-2525-41dd-a7a5-34e5daa8dc2e')
                        title = "Hai un nuovo appuntamento 🙂"
                        cont =   "Il  giorno " +str(self.request.data['day'])+ " "  + months[self.request.data['month']] + " alle " + times[start_t] +" presso " + shop.store_name
                        payload = {"app_id": "91f9f284-1a50-44c4-8d5d-7ff9102e75a0",
                                "include_player_ids":ids ,
                                "headings": {"en": title},
                                "contents": {"en": cont}}
                        requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                    serializer.save(client=client)
                    serializer.save(shop=shop)
                 
                    serializer.save(details=details,start=start, end=end, start_t=start_t, end_t=end_t,day_to_delete=shop.cancel_advance,store_phone=shop.phone_number,store_name=shop.store_name,location=shop.address)
        else:
           
            raise serializers.ValidationError({'just_booked': True})
            raise Response({'just_booked': True}, status=400)

class BookingsShadowAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class = BookingsSerializer

    def perform_create(self, serializer):
        details = self.request.data['details']
        if 'new' in self.request.data:
            start_t = self.request.data['start']
            end_t = self.request.data['end']
            start = (start_t-9)/3
            end = start + (end_t - start_t)

        else:
            start = self.request.data['start']
            end = self.request.data['end']
            start_t = times.index(rows[self.request.data['start']])
            end_t = start_t+ self.request.data['end'] - self.request.data['start']

        if Bookings.objects.filter( employee=self.request.data['employee'], day=self.request.data['day'], month=self.request.data['month'], year=self.request.data['year'], start_t__lt=end_t,end_t__gt=start_t).first() == None:
            if int(self.request.data['service_n'])>0 :
                service_id = self.request.data['service_n']
                service = ServicesStore.objects.filter(id=service_id).first()
                if self.request.data['month'] >4 and self.request.data['month'] < 9:
                    price = service.price_2
                else:
                    price = service.price

                if 'adons' in self.request.data :
                    adons_list = self.request.data['adons']
                    for adon_id in adons_list:
                        adon = AddOn.objects.filter(id=adon_id).first()
                        details = details + ' + ' + adon.name
                        price= price + adon.price
                serializer.save(price=price)


            if StoreClient.objects.filter(shop=self.request.data['shop'], client=self.request.user).first() == None:
                if self.request.data['employee'] != self.request.user:
                    shop = Store.objects.filter(id=self.request.data['shop']).first()
                    StoreClient.objects.create(shop=shop, client_name=self.request.data['client_name'], client=self.request.user, phone=self.request.data['phone'], note='Ultimo servizio: '+details,)
            shop = Store.objects.filter(id=self.request.data['shop']).first()
            serializer.save(store_phone=shop.phone_number,store_name=shop.store_name,location=shop.address, shop=shop,client=self.request.user,day_to_delete=shop.cancel_advance,visible=False)
            serializer.save(details=details,start=start,end=end, start_t=start_t, end_t=end_t,booked_on_plt=True)
        else:
           
            raise serializers.ValidationError({'just_booked': True})
            raise Response({'just_booked': True}, status=400)



class BookingsWeekAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]

    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"
    def get_queryset(self,):
        owner = self.request.GET['owner']
        week = self.kwargs.get(self.lookup_url_kwarg)
        year=datetime.datetime.now().year
        shop=Store.objects.filter(owner=owner).first()
        qs = Bookings.objects.filter(shop=shop, week=week, visible=True, year__gte = year,).all().order_by('month', 'day', 'start')
        return qs

class BookingsPayFromShopAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = BookingsSerializer


    def get_queryset(self,):
        id=self.request.GET['id']
        shop=Store.objects.filter(owner=self.request.user).first()
        qs = Bookings.objects.filter(shop=shop, id=id).update(payed=True)
        return []

class BookingsWeekExternalAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"
    def get_queryset(self,):
        owner = self.request.GET['owner']
        week = self.kwargs.get(self.lookup_url_kwarg)
        shop=Store.objects.filter(owner=owner).first()
        year=datetime.datetime.now().year
        qs = Bookings.objects.filter(week__gte = week ,year__gte = year,  shop = shop, visible=True,booked_on_plt=True).order_by('month', 'day', 'start')
        # qs = Bookings.objects.filter(week = week , shop = shop).filter(~Q(client=owner)).order_by('month', 'day', 'start')
        return qs

class BookingsWeekByShopAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"
    def get_queryset(self,):
        shop = self.request.GET['shop']
        week = self.kwargs.get(self.lookup_url_kwarg)
        qs = Bookings.objects.filter(shop=shop, week=week, visible=True).all().order_by('month', 'day', 'start')
        return qs

class Bookings2WeeksByShopAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"
    def get_queryset(self,):
        shop = self.request.GET['shop']
        week = self.kwargs.get(self.lookup_url_kwarg)
        week_b = week+1
        qs = Bookings.objects.filter(shop=shop, week__gte=week, week__lte=week_b, visible=True).all().order_by('month', 'day', 'start')
        return qs

class Bookings5WeeksByShopAPIView(generics.ListAPIView):
    permission_classes      = [AllowAny]
    
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"
    def get_queryset(self,):
        shop = self.request.GET['shop']
        week = self.kwargs.get(self.lookup_url_kwarg)
        week_b = week+4
        qs = Bookings.objects.filter(shop=shop, week__gte=week, week__lte=week_b, year=2021,visible=True).all().order_by('month', 'day', 'start')
        return qs


class BookingsMonthAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "month"
    def get_queryset(self,):
        month = self.kwargs.get(self.lookup_url_kwarg)
        own_shop=Store.objects.filter(owner=self.request.user).first()
        qs = Bookings.objects.filter(shop=own_shop, month=month, visible=True).all()
        return qs

class BookingsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset             = Bookings.objects.all()
    serializer_class     = BookingsSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]

    def update(self, request, pk,*kwarg):

        if 'new' in self.request.data:
            start_t = self.request.data['start']
            end_t = self.request.data['end']
            start = (self.request.data['start']-9)/3
            end = start + (end_t - start_t)

        else:
            start = self.request.data['start']
            end = self.request.data['end']
            start_t = times.index(rows[self.request.data['start']])
            end_t = start_t+ self.request.data['end'] - self.request.data['start']

        shop = Store.objects.filter(owner=self.request.user).first()
        old_appo = Bookings.objects.filter(id=pk).first()

        if 'client_id' in self.request.data:
            Bookings.objects.filter(id=pk).update(start=start , end=end, start_t=start_t, end_t=end_t, client=self.request.data['client_id'],day=self.request.data['day'], week=self.request.data['week'], month=self.request.data['month'], year=self.request.data['year'],employee=self.request.data['employee'], client_name=self.request.data['client_name'], details=self.request.data['details'], service_n=self.request.data['service_n'],phone=self.request.data['phone'],note=self.request.data['note'])
        else:
            Bookings.objects.filter(id=pk).update(start=start , end=end, start_t=start_t, end_t=end_t,day=self.request.data['day'], week=self.request.data['week'], month=self.request.data['month'], year=self.request.data['year'],employee=self.request.data['employee'], client_name=self.request.data['client_name'], details=self.request.data['details'], service_n=self.request.data['service_n'],phone=self.request.data['phone'],note=self.request.data['note'])

        service_id = self.request.data['service_n']
        service = ServicesStore.objects.filter(id=service_id).first()
        if self.request.data['month'] >4 and self.request.data['month'] < 9:
            new_price = service.price_2
        else:
            new_price = service.price

        if old_appo.shop == shop:
            if shop.update_price_scroll:
                new_price = new_price * (end_t - start_t)/service.duration
                Bookings.objects.filter(id=pk).update(price=new_price)
            if 'payed' in self.request.data:
                Bookings.objects.filter(id=pk).update(payed=self.request.data['payed'])
            if 'store_client' in self.request.data:
                Bookings.objects.filter(id=pk).update(store_client=self.request.data['store_client'])
        Bookings.objects.filter(id=pk).update(price=new_price)
        qs1= Bookings.objects.filter(id=pk).first()
        ser = BookingsSerializer(qs1,many=False)
        return Response(ser.data)

    def delete(self, request, pk):
        qs = Bookings.objects.filter(id=pk).first()
        # Bookings.objects.filter(id=pk).update(visible=False)

        shop = qs.shop
        months_names=['Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
        header = {"Content-Type": "application/json; charset=utf-8"}
        devices = UserDevice.objects.filter(user=qs.employee)
        ids=[]
        for device in devices:
            ids.append(device.player_id)
        ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
        ids.append('31472672-5cbd-4af1-bc8b-d514aa8045bd')
        title= shop.store_name+": Prenotazione annullata "
        cont = 'La prenotazione di ' + qs.client_name + ' è  stata cancellata!\nData: '+ str(qs.day) +' '+months_names[qs.month]+' '+ str(qs.year) +' alle '+ times[qs.start_t] +'\n\n( ' +self.request.user.email+' )'
        payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                "include_player_ids":ids ,
                "headings": {"en": title},
                "contents": {"en": cont}}
        requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        qs.delete()
        return Response({'message': "Cancellato"}, status=203)


class BookingsUserAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = BookingsSerializer

    def get_queryset(self,):
        client = self.request.GET['user']
        qs = Bookings.objects.filter(client=client,  visible=True).all().order_by('month', 'day', 'start')
        return qs

class BookingsUserWeekAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = BookingsSerializer
    lookup_url_kwarg        = "week"

    def get_queryset(self,):
        week = self.kwargs.get(self.lookup_url_kwarg)
        client = self.request.GET['user']

        year=self.request.GET['year']
        qs = Bookings.objects.filter(Q(client=client, week__gte=week, year__gte=year, visible=True ) | Q(client=client, year__gt=year, visible=True)).all().order_by('year', 'month', 'day', 'start')
        return qs

class BookingsAggregateAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = BookingsLightSerializer

    def get(self, request, format=None):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        if own_shop == None:
            raise Response({'message': "Non sei autorizzato"}, status=400)
        month = self.request.GET['month']
        year = self.request.GET['year']
        bookings = Bookings.objects.filter(month=month, year=year, shop=own_shop, visible=True)
        serializer = BookingsLightSerializer(bookings, many=True)
        return Response(serializer.data)


class BookRecurringAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class = BookingsSerializer

    def post(self, request, format=None):
        own_shop=Store.objects.filter(owner=self.request.user).first()
        if own_shop == None:
            raise Response({'message': "Non sei autorizzato"}, status=400)

        Bookings.objects.filter(id=self.request.data['id']).update(recurring_id=self.request.data['id'])
        booking = Bookings.objects.filter(id=self.request.data['id']).first()
        appo_date =  datetime.datetime(booking.year, booking.month+1, booking.day)
        # weeks = int(self.request.data['weeks'])+1

        if 'payed' in self.request.data:
            payed = self.request.data['payed']
        else:
            payed = False
        days_booked ='Giorni'
        for x in range(1,int(self.request.data['weeks'])+1):
            new_appo_date = appo_date + timedelta(days=7*x)
            data={
            'shop':booking.shop.id,
            'client':booking.client.id,
            'employee':booking.employee.id,
            'start':booking.start,
            'end' :booking.end,
            'start_t':booking.start_t,
            'end_t' :booking.end_t,
            'day' :new_appo_date.day,
            'week':new_appo_date.isocalendar()[1],
            'month' :new_appo_date.month-1,
            'year':new_appo_date.year,
            'address':booking.address,
            'location':booking.location,
            'client_name' :booking.client_name,
            'store_name':booking.store_name,
            'store_phone':booking.store_phone,
            'phone':booking.phone,
            'note':booking.note,
            'details' :booking.details,
            'service_n':booking.service_n,
            'recurring_id':booking.id,
            'store_client':booking.store_client,
            'price':booking.price,
            'payed':payed,
            'day_to_delete':booking.day_to_delete
            }
            serializer_new = BookingsSerializer(data=data)

            if Bookings.objects.filter( employee=data['employee'], day=data['day'], month=data['month'], year=data['year'], start_t__lt=data['end_t'],end_t__gt=data['start_t']).first() == None:
                if serializer_new.is_valid():
                    serializer_new.save()
                    serializer_new.save(payed=payed)
                    serializer_new.save(price=booking.price)
                    # serializer_new.save(client=client_tag)
                else:
                    raise ValidationError(serializer_new.errors)
            else:
                days_booked=days_booked+' - '+ str(data['day'])+' '+ months[data['month']]+' '+ str(data['year'])

        return Response({'days_booked': days_booked}, status=200)

class BookingsRecurringDeleteAPIView(generics.DestroyAPIView):
    queryset             = Bookings.objects.all()
    serializer_class     = BookingsSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        week=self.request.GET['week']
        year=self.request.GET['year']
        qs = Bookings.objects.filter(recurring_id=pk, week__gte=week, year__gte=year).all()
        qs.delete()
        return Response({'message': "Cancellato"}, status=203)


class SendBookingNotificationView(generics.ListAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        queryset                = Bookings.objects.all()
        serializer_class        = BookingsSerializer

        def get(self, request, format=None):
            client = self.request.user.id
            bookings_ids_string = self.request.GET['list_ids']
            bookings_id= bookings_ids_string.split(",")
            header = {"Content-Type": "application/json; charset=utf-8",
                    }
            for appo_id in bookings_id:
                appointment = Bookings.objects.filter(id=appo_id,client=client).first()
                if bookings_id.index(appo_id) == 0:
                    # shop=Store.objects.filter(id=appointment.shop).first()
                    devices = UserDevice.objects.filter(user=appointment.shop['owner'])
                    title = appointment.shop['store_name'] +": Nuova prenotazione 🙂"
                    ids=[]
                    for device in devices:
                        ids.append(device.player_id)
                    ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
                    ids.append('a416d507-a073-4ec5-983b-cd6dff542160')
                    ids.append('2be8c721-b0af-4dbd-8502-2647e754f61e')
                cont =  appointment.client_name+" " + appointment.details+  " il " +str(appointment.day)+ " "  + months[appointment.month] + " alle " + times[appointment.start_t]
                not_data ={"day":appointment.day,"month":appointment.month,"year":appointment.year,"start":appointment.start_t,"employee":appointment.employee}
                payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "data": not_data,
                        "contents": {"en": cont}}
                requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            return Response({'sent': True}, status=200)


class DeleteShadowsView(generics.DestroyAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        queryset                = Bookings.objects.all()
        serializer_class        = BookingsSerializer

        def delete(self, request, format=None):
            client = self.request.user.id
            bookings_ids_string = self.request.GET['list_ids']
            bookings_id= bookings_ids_string.split(",")
            for appo_id in bookings_id:
                appointment = Bookings.objects.filter(id=appo_id,client=client).delete()
            return Response({'sent': True}, status=200)

# class FastUpdateView(generics.ListAPIView):
#     permission_classes      = [AllowAny]
#     queryset                = Bookings.objects.all()
#     serializer_class        = BookingsSerializer

#     def get(self, request, format=None):
#         appointments = Bookings.objects.filter(recurring_id__gte=10,price=0,service_n__gte=1, shop=36).all()
#         for appo in appointments:
#             priced_appo = Bookings.objects.filter(id=appo.recurring_id).first()
#             if priced_appo != None:
#                 Bookings.objects.filter(id=appo.id).update(price=priced_appo.price)
#         return Response({'sent': True}, status=200)
