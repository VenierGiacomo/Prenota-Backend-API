from rest_framework import generics
import os
from .serializers import StripeDataSerializer
from services.models import ServicesStore
from webhooks.models import StripeData
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from userdevices.models import UserDevice
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
import stripe
from store.models import Store
from shopclients.models import StoreClient
import math
from bookings.models import Bookings
rows = ["06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "20:45", "21:00", "21:15", "21:30", "21:45", "22:00", "22:15", "22:30", "22:45", "23:00", "23:15", "23:30", "23:45", "24:00"]
months=['Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
import json
import requests
import pusher

class StripeWeebhookAPIView(generics.ListCreateAPIView):
    permission_classes      = [AllowAny]
    queryset                = StripeData.objects.all()
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
        stripe.api_key = os.environment.get('STRIPE_SK')
        

        webhook_secret = os.environment.get('STRIPE_WHSK')
  
        
        raw_body = request.body
        payload = request.data
        data = payload['data']
        event_type = payload['type']
        data_object =  data['object']
        customer = data_object['customer']
        connectedAccountId = data_object['transfer_data']['destination']

        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                raw_body, sig_header, webhook_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed .' + str(e))
            return Response({'Success': True}, status=200)

        if event_type == 'charge.succeeded':
            ser = {}
            ser['hook_type']=event_type
            if 'destination' in data_object :
                ser['data_string']="Shop: " + data_object['destination'] + " - " + data_object['description'] + " time " + str(data_object['created'])
            else:
                ser['data_string']="Shop: " + data_object['billing_details']['email'] + " - " + data_object['description'] + " time " + str(data_object['created'])

            ser['client']=customer
            serializer = StripeDataSerializer(data=ser)
            transfers = stripe.Transfer.list(
                                destination = connectedAccountId,
                                transfer_group = data_object['transfer_group'],
            );

            paymentId = transfers.data[0].destination_payment;

            ids_list = data_object['description'].split('- ids:')[1].split()
            header = {"Content-Type": "application/json; charset=utf-8",
                    }
            for id_str in ids_list:
                appointment = Bookings.objects.filter(id=int(id_str)).first()
                if(appointment.visible == False):
                    shop = appointment.shop
                    devices = UserDevice.objects.filter(user=shop.owner)
                    ids=[]
                    for device in devices:
                        ids.append(device.player_id)
                    ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
                    ids.append('a416d507-a073-4ec5-983b-cd6dff542160')
                    ids.append('2be8c721-b0af-4dbd-8502-2647e754f61e')


                    title = shop.store_name +": Nuova prenotazione 🙂"
                    cont =  appointment.client_name+" " + appointment.details +  " il " +str(appointment.day)+ " "  + months[appointment.month] + " alle " + rows[appointment.start]
                    not_data ={"day":appointment.day,"month":appointment.month,"year":appointment.year,"start":appointment.start_t,"employee":appointment.employee.id}
                    payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                    "include_player_ids":ids ,
                    "headings": {"en": title},
                    "data": not_data,
                    "contents": {"en": cont}}
                    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                Bookings.objects.filter(id=int(id_str)).update(payed=True, visible=True)

            if serializer.is_valid():
                serializer.save()
                header = {"Content-Type": "application/json; charset=utf-8",
                    
                    }
                ids=[]
                ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
                ids.append('a416d507-a073-4ec5-983b-cd6dff542160')
                ids.append('2be8c721-b0af-4dbd-8502-2647e754f61e')

                formatted_float = "{:,.2f}€".format(data_object['amount']/100)
                title = "💸 Nuovo pagamento 💸"
                cont =  "Hai guadagnato "+ formatted_float + " su Prenota"
                payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "contents": {"en": cont}}
                requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                stripe.Charge.modify(
                paymentId,
                  description= data_object['description'],
                  stripe_account=connectedAccountId,
            );
                return Response({'Success': True}, status=200)
            return Response(serializer.errors, status=400)

        if event_type == 'charge.failed':
            ser = {}
            ser['hook_type']=event_type
            if 'destination' in data_object :
                ser['data_string']="Shop: " + data_object['destination'] + " - " + data_object['description'] + " time " + str(data_object['created'])
            else:
                ser['data_string']="Shop: " + data_object['billing_details']['email'] + " - " + data_object['description'] + " time " + str(data_object['created'])
            ser['client']=customer
            serializer = StripeDataSerializer(data=ser)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': True}, status=200)
            return Response(serializer.errors, status=400)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentmethodsAPIView(generics.CreateAPIView):
        permission_classes      = [AllowAny]
        queryset                = StripeData.objects.all()
        serializer_class        = StripeDataSerializer

        def post(self, request, format=None):
            stripe.api_key = os.environment.get('STRIPE_SK')
            
            User = get_user_model()
            if self.request.user.id:
                user = User.objects.filter(id=self.request.user.id).first()
                if user.stripe_customer_id is None:
                    customer = stripe.Customer.create()
                    User.objects.filter(id=self.request.user.id).update(stripe_customer_id=customer.id)
                    payment_method = stripe.PaymentMethod.list(
                    customer=customer.id,
                    type="card",
                    )
                    ser = {}
                    ser['hook_type']='request_payment_methods'
                    ser['data_string']=customer.id
                    ser['client']=self.request.user.id
                    serializer = StripeDataSerializer(data=ser)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'data': payment_method.data}, status=200)
                    return Response({'status': "You do not have a stripe_id yet"}, status=200)
                else:
                    payment_method = stripe.PaymentMethod.list(
                    customer=user.stripe_customer_id,
                    type="card",
                    )
                    ser = {}
                    ser['hook_type']='request_payment_methods'
                    ser['data_string']=user.stripe_customer_id
                    ser['client']=self.request.user.id
                    serializer = StripeDataSerializer(data=ser)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'data': payment_method.data}, status=200)
                    return Response(serializer.errors, status=400)
            else:
                return Response({'status': "You are not logged in yet"}, status=200)


class ListTransactionsAPIView(generics.ListAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        queryset                = StripeData.objects.all()
        serializer_class        = StripeDataSerializer

        def get(self, request, format=None):
            stripe.api_key = os.environment.get('STRIPE_SK')
            
            store = Store.objects.filter(owner=self.request.user.id).first()
            transactions = stripe.BalanceTransaction.list(limit=30, stripe_account=store.stripe_connect, type="payment")
            return Response( transactions, status=200)

class BusTriesteTicketAPIView(generics.CreateAPIView):
        permission_classes      = [AllowAny]
        queryset                = StripeData.objects.all()
        serializer_class        = StripeDataSerializer

        def post(self, request, format=None):
            # stripe.api_key = os.environment.get('STRIPE_SK')
            stripe.api_key = 'sk_test_m1iAyTS2cTQCtBzFH0ReqqjX0092AIJkIy'
            Users = get_user_model()
            fee = math.ceil(3575/100*3.5)
            if self.request.user.id:
                customer = Users.objects.filter(id=self.request.user.id).first()
                if customer.stripe_customer_id is None:
                    return Response({'status': "You do not have a stripe_id yet"}, status=200)
                else:
                    intent = stripe.PaymentIntent.create(
                      amount=3575,
                      currency='eur',
                      customer=customer.stripe_customer_id,
                      receipt_email=customer.email,
                      application_fee_amount=fee,
                      transfer_data={
                        'destination': 'acct_1IAZ28E1tqHkCQkv',
                      },
                    )
                    ser = {}
                    ser['hook_type']='request_payment_intent'
                    ser['data_string']=intent.amount
                    ser['client']=self.request.user.id
                    serializer = StripeDataSerializer(data=ser)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'client_secret': intent.client_secret}, status=200)
                    return Response(serializer.errors, status=400)
            else:
                customer = stripe.Customer.create()
                intent = stripe.PaymentIntent.create(
                  amount=3575,
                  currency='eur',
                  customer=customer['id'],
                  receipt_email="giacomo.venier@gmail.com",
                  application_fee_amount=fee,
                      transfer_data={
                        'destination': 'acct_1IAZ28E1tqHkCQkv',
                      },
                )
                ser = {}
                ser['hook_type']='request_payment_ticket'
                ser['data_string']='anonymous'
                ser['client']=0
                serializer = StripeDataSerializer(data=ser)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'client_secret': intent.client_secret}, status=200)
                return Response(serializer.errors, status=400)




class PayShopFromBooking(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = StripeData.objects.all()
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
            stripe.api_key = os.environment.get('STRIPE_SK')
            
            User = get_user_model()
            bookings_id = self.request.data['list_ids']
            tot = 0
            description = ''
            list_ids= ''
            for appo_id in bookings_id:
                appointment = Bookings.objects.filter(id=appo_id).first()
                tot = tot + appointment.price
                description = description + appointment.details +' & '
                client_name = appointment.client_name
                day = appointment.day
                month = appointment.month+1
                year = appointment.year
                list_ids = list_ids + str(appo_id)+' '
            description = description[:-3]
            description = description + ' - ' + client_name + ' - ' +str(day) +'/'+ str(month) +'/'+str( year) +' - ids: ' +list_ids
            fee = math.ceil(tot/100*2.4)+25
            shop = appointment.shop
            user = User.objects.filter(id=self.request.user.id).first()
            print(description, tot)
            if user.stripe_customer_id == None or len(user.stripe_customer_id)<4:
                 customer = stripe.Customer.create()
                 User.objects.filter(id=self.request.user.id).update(stripe_customer_id=customer.id)
                 intent = stripe.PaymentIntent.create(
                  amount=tot,
                  currency='eur',
                  customer=customer.id,
                  receipt_email=user.email,
                  application_fee_amount=fee,
                  description= description,
                  setup_future_usage='off_session',
                  transfer_data={
                    'destination': shop.stripe_connect,
                  },
                )
            else:
                intent = stripe.PaymentIntent.create(
                  amount=tot,
                  currency='eur',
                  customer=user.stripe_customer_id,
                  receipt_email=user.email,
                  application_fee_amount=fee,
                  description = description,
                  setup_future_usage='off_session',
                  transfer_data={
                    'destination': shop.stripe_connect,
                  },
                )
            ser = {}
            ser['hook_type']='pay_shop_intent'
            ser['data_string']=tot
            ser['client']=self.request.user.id
            serializer = StripeDataSerializer(data=ser)
            if serializer.is_valid():
                serializer.save()
                return Response({'client_secret': intent.client_secret, 'tot': tot}, status=200)
            return Response(serializer.errors, status=400)



class StripeSessionAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = StripeData.objects.all()
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
        stripe.api_key = os.environment.get('STRIPE_SK')
        
        Users = get_user_model()
        customer = Users.objects.filter(id=self.request.user.id).first()
        session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        payment_method_types=["card"],
        customer=customer.stripe_customer_id,
        line_items=[
            {
              "price": "price_HJ483KkKFlocQk",
              "quantity": 1,
            },
        ],

        mode="subscription",
        )
        ser = {}
        ser['hook_type']='subscription_initiated'
        ser['data_string']='price_HJ483KkKFlocQk'
        ser['client']=self.request.user.id
        serializer = StripeDataSerializer(data=ser)
        if serializer.is_valid():
            serializer.save()
            return Response({'session_id': session.id}, status=200)
        return Response(serializer.errors, status=400)


class StripeCustomerPortalAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = StripeData.objects.all()
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
        stripe.api_key = os.environment.get('STRIPE_SK')
        
        Users = get_user_model()
        customer = Users.objects.filter(id=self.request.user.id).first()
        session = stripe.billing_portal.Session.create(
        customer=customer.stripe_customer_id,
      )
        ser = {}
        ser['hook_type']='portal_initiated'
        ser['data_string']=customer.email
        ser['client']=self.request.user.id
        serializer = StripeDataSerializer(data=ser)
        if serializer.is_valid():
            serializer.save()
            return Response( session, status=200)
        return Response(serializer.errors, status=400)


class StripeActivateConnect(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = StripeData.objects.all()
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
        stripe.api_key = os.environment.get('STRIPE_SK')
        Users = get_user_model()
        customer = Users.objects.filter(id=self.request.user.id).first()
        store = Store.objects.filter(owner=self.request.user.id).first()
        if customer.sex=='m':
            gender='male'
        else:
            gender='female'
        if store.stripe_connect is None:
            if self.request.data['business_type'] == "individual":
                account = stripe.Account.create(
                                              type="standard",
                                              country="IT",
                                              email=customer.email,
                                              default_currency='EUR',
                                              business_profile={
                                                    "name": store.store_name,
                                                    "product_description": store.business_description,
                                                    "support_address":{
                                                    "city":"Trieste",
                                                    "country":"IT",
                                                    "line1":store.address,
                                                    "postal_code":store.zip_code,
                                                    "state":"Trieste",
                                                  },
                                                  "support_email":"business@prenota.cc",
                                                  "support_phone":"+393404526854",
                                                  "support_url":"https://prenota.cc",
                                                  "url":store.website,
                                              },
                                              business_type="individual",
                                              individual={
                                                  "address":{
                                                    "city":"Trieste",
                                                    "country":"IT",
                                                    "line1":store.address,
                                                    "postal_code":store.zip_code,
                                                    "state":"Trieste",
                                                  },
                                                  "email":customer.email,
                                                  "first_name":customer.first_name,
                                                  "gender":gender,
                                                  "last_name":customer.last_name,
                                                  "phone":customer.phone,
                                              },
                                            )
            else:
                account = stripe.Account.create(
                                              type="standard",
                                              country="IT",
                                              email=customer.email,
                                              default_currency='EUR',
                                              business_profile={
                                                    "name": store.store_name,
                                                    "product_description": store.business_description,
                                                    "support_address":{
                                                    "city":"Trieste",
                                                    "country":"IT",
                                                    "line1":store.address,
                                                    "postal_code":store.zip_code,
                                                    "state":"Trieste",
                                                  },
                                                  "support_email":"business@prenota.cc",
                                                  "support_phone":"+393404526854",
                                                  "support_url":"https://prenota.cc",
                                                  "url":store.website,
                                              },
                                              business_type="company",
                                              company={
                                                  "address":{
                                                    "city":"Trieste",
                                                    "country":"IT",
                                                    "line1":store.address,
                                                    "postal_code":store.zip_code,
                                                    "state":"Trieste",
                                                  },
                                                  "name": store.store_name,
                                                  "phone":customer.phone,
                                              },
                                            )
            Store.objects.filter(owner=self.request.user.id).update(stripe_connect=account.id)
            account_links = stripe.AccountLink.create(
                                                    account=account.id,
                                                    refresh_url='https://prenota.cc/refresh_account',
                                                    return_url='https://prenota.cc/settings',
                                                    type='account_onboarding',
                                                    )
        else:
            account_links = stripe.AccountLink.create(
                                                    account=store.stripe_connect,
                                                    refresh_url='https://prenota.cc/refresh_account',
                                                    return_url='https://prenota.cc/settings',
                                                    type='account_onboarding',
                                                    )
        ser = {}
        ser['hook_type']='starting_business_account'
        ser['data_string']=customer.email
        ser['client']=self.request.user.id
        serializer = StripeDataSerializer(data=ser)
        if serializer.is_valid():
            serializer.save()
            return Response( account_links, status=200)
        return Response(serializer.errors, status=400)


class PayShopWithCreditBooking(generics.CreateAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        queryset                = StripeData.objects.all()
        serializer_class        = StripeDataSerializer

        def post(self, request, format=None):
            client = self.request.user.id
            bookings_id = self.request.data['list_ids']
            tot = 0
            header = {"Content-Type": "application/json; charset=utf-8",
                    }
            for appo_id in bookings_id:
                appointment = Bookings.objects.filter(id=appo_id, client=client).first()
                shop = appointment.shop
                tot = tot + appointment.price
                ids=[]
                if(appointment.visible == False):
                    devices = UserDevice.objects.filter(user=shop.owner)

                    for device in devices:
                        ids.append(device.player_id)
                    ids.append('1f80985d-fa71-4010-a925-3861907a6b64')
                    ids.append('a416d507-a073-4ec5-983b-cd6dff542160')
                    ids.append('2be8c721-b0af-4dbd-8502-2647e754f61e')

                    title = shop.store_name +": Nuova prenotazione 🙂"
                    cont =  appointment.client_name+" " + appointment.details +  " il " +str(appointment.day)+ " "  + months[appointment.month] + " alle " + rows[appointment.start]
                    not_data ={"day":appointment.day,"month":appointment.month,"year":appointment.year,"start":appointment.start_t,"employee":appointment.employee.id}
                    payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                    "include_player_ids":ids ,
                    "headings": {"en": title},
                    "data": not_data,
                    "contents": {"en": cont}}
                    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

            storeclient = StoreClient.objects.filter(shop=shop, client=client).first()
            new_customer_balance = storeclient.credit - tot
            if new_customer_balance >= 0:
                StoreClient.objects.filter(shop=shop, client=client).update(credit=new_customer_balance)
                for appo_id in bookings_id:
                    appointment = Bookings.objects.filter(id=appo_id, client=client).update(payed=True, visible=True)

                ser = {}
                ser['hook_type']='pay_shop_with_credit'
                ser['data_string']=tot
                ser['client']=self.request.user.id
                serializer = StripeDataSerializer(data=ser)
                if serializer.is_valid():
                    serializer.save()

                    formatted_float = "{:,.2f}€".format(tot/100)
                    title = "💸 Nuovo pagamento 💸"
                    cont =  "Hai guadagnato "+ formatted_float + " su Prenota"
                    payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                        "include_player_ids":ids ,
                        "headings": {"en": title},
                        "contents": {"en": cont}}
                    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                    return Response({'payed': True, 'tot': tot}, status=200)
                return Response({'payed': False, 'tot': tot}, status=400)
            return Response({'payed': False, 'tot': tot}, status=400)


class newCustomeRequestAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StripeDataSerializer

    def post(self, request, format=None):
        client = StoreClient.objects.filter(shop=self.request.data['shop_id'], client=self.request.user).first()
        if client is None:
            pusher_client = pusher.Pusher(
              app_id='1161409',
              key='45f982633227395f42a9',
              secret='539affddd1466113919b',
              cluster='eu',
              ssl=True
            )
            name = self.request.user.first_name + ' ' +self.request.user.last_name
            pusher_client.trigger(self.request.data['channel'], 'become-costumer', {'message': name, 'id': self.request.user.id})
            ser = {}
            ser['hook_type']='new_customer_socket'
            ser['data_string']=self.request.data['channel']
            ser['client']=self.request.user.id
            serializer = StripeDataSerializer(data=ser)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'sent','already_exist': False}, status=200)
            return Response({'status': 'failed','already_exist': False}, status=400)
        else:
            return Response({'status': 'failed','already_exist': True}, status=400)





class selfNotificationsAPIView(generics.ListAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    serializer_class        = StripeDataSerializer

    def get(self, request, format=None):
        header = {"Content-Type": "application/json; charset=utf-8"}
        devices = UserDevice.objects.filter(user=self.request.user)
        ids=[]
        for device in devices:
            ids.append(device.player_id)
        title = "Le notifiche funzionano! 🙂"
        cont =  "Ora puoi ricevere le notifiche per tutti i tuoi apputnamenti"
        payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
                "include_player_ids":ids ,
                "headings": {"en": title},
                "contents": {"en": cont}}
        res = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(res)
        return Response({'status': 'sent'}, status=200)







