from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import EmailConfirmSerializer, RegisterconfirmationSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from store.models import Store
from django.template.loader import render_to_string

class ConfirmBookingsAPIView(generics.CreateAPIView):
        permission_classes      = [IsAuthenticated]
        authentication_classes  = [JSONWebTokenAuthentication]
        serializer_class = EmailConfirmSerializer

        def perform_create(self, serializer):
            data=self.request.data
            serializer.save()
            email_from = settings.DEFAULT_FROM_EMAIL
            store = Store.objects.filter(store_name=data['shop']).first()
            if store is None:
                # if(data['shop']!="Aparrucchieri"):
                html_message = render_to_string('email_template_no_address.html',{'surname': data['surname'], 'name': data['name'], 'day':data['day'], 'month': data['month'], 'year': data['year'], 'shop': data['shop'], 'time':data['time'], 'address':''})
                subject = data['shop']+' | Prenotazione effettuata in data '+ str(data['day']) +' '+ data['month'] +' '+ str(data['year'])
                message = 'Conferma di prenotazione:\n\nGentile '+data['surname']+' '+ str(data['name'])  +', il suo appuntamento è stato fissato in data '+ str(data['day']) +' '+ data['month'] +' '+ str(data['year']) + ' alle '+ data['time'] + ' presso lo studio ' + data['shop'] +"\n\nPuò vedere i suoi appuntamenti accedendo a : https://prenota.cc/i_miei_appuntamenti \n\nO scaricando l'app:\n\niOS: https://apps.apple.com/app/id1523525291\n\nAndroid:http://play.google.com/store/apps/details?id=io.prenota.client"
                recipient_list = [data['email']]
                send_mail( subject, message, email_from, recipient_list, html_message=html_message  )
            else:
                if(data['shop']!="Circolo Tennis Grignano"):
                    html_message = render_to_string('email_booking.html',{'surname': data['surname'], 'name': data['name'], 'day':data['day'], 'month': data['month'], 'year': data['year'], 'shop': data['shop'], 'time':data['time'], 'address':store.address})
                    subject =  data['shop']+' | Prenotazione effettuata in data '+ str(data['day']) +' '+ data['month'] +' '+ str(data['year'])
                    message = 'Conferma di prenotazione:\n\nGentile '+data['surname']+' '+ str(data['name'])  +', il suo appuntamento è stato fissato in data '+ str(data['day']) +' '+ data['month'] +' '+ str(data['year']) + ' alle '+ data['time'] + ' presso lo studio ' + data['shop'] + "in via "+ store.address + "\n\nPuò vedere i suoi appuntamenti accedendo a : https://prenota.cc/i_miei_appuntamenti \n\nO scaricando l'app:\n\niOS: https://apps.apple.com/app/id1523525291\n\nAndroid:http://play.google.com/store/apps/details?id=io.prenota.client"
                    recipient_list = [data['email']]
                    send_mail( subject, message, email_from, recipient_list, html_message=html_message  )
            # subject1 =  data['shop'] +' nuova prenotazione di '+ str(data['name']) +' '+ data['surname']
            # message1 = str(data['name']) +' '+ data['surname'] +' ha prenotato in data '+ str(data['day']) +' '+ data['month'] +' '+ str(data['year']) + ' alle '+ data['time'] + ' presso lo studio ' + data['shop']
            # recipient_list1 = ['giacomo.venier@gmail.com','franz.stupar@gmail.com']
            # send_mail( subject1, message1, email_from, recipient_list1)

class ConfirmRegistrationAPIView(generics.CreateAPIView):
        permission_classes = [AllowAny]
        serializer_class = RegisterconfirmationSerializer

        def perform_create(self, serializer):
            data=self.request.data
            serializer.save()
            subject = 'Nuovo Business registered skuu!'
            message = data['name']+ ' ' + data['surname'] + '\n\nemail: ' + data['email'] + '\n\ntelefono: '+ data['phone']+ '\n\nNuova registrazione. Chiama asap!'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['giacomo.venier@gmail.com','franz.stupar@gmail.com', 'business@prenota.cc', 'giacomo@prenota.cc']
            send_mail( subject, message, email_from, recipient_list)