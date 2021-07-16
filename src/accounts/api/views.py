from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from store.models import Store
from employees.models import Employee
from .serializers import StdUserRegisterSerializer, EmployeeRegisterSerializer, StdUserUpdaterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
import stripe
import os
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys




User = get_user_model()

class StdRegisterAPIView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = StdUserRegisterSerializer
    permission_classes  = [AllowAny]

    def post(self, request, format=None):
            serializer = StdUserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                name = request.data["first_name"]+' '+request.data["last_name"]
                stripe.api_key = os.environment.get('STRIPE_SK')
                customer = stripe.Customer.create(
                    phone=  request.data["phone"],
                    email=  request.data["email"],
                    name = name,
                    )
                serializer.save(stripe_customer_id=customer.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DetailAccountAPIView(generics.RetrieveUpdateAPIView):
    queryset            = User.objects.all()
    serializer_class    = StdUserUpdaterSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]


class EmployeeRegisterAPIView(generics.CreateAPIView):
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [JSONWebTokenAuthentication]
    queryset                = User.objects.all()
    serializer_class        = EmployeeRegisterSerializer


    def post(self, request, format=None):
            serializer = EmployeeRegisterSerializer(data=request.data)
            if serializer.is_valid():
                employee = serializer.save()
                shop_id = Store.objects.filter(owner=self.request.user).first()
                name = request.data["first_name"]
                Employee.objects.create(shop=shop_id, employee=employee, name=name)
                
                # customer = stripe.Customer.create()
                # Set your secret key. Remember to switch to your live secret key in production!
                # See your keys here: https://dashboard.stripe.com/account/apikeys
                # pay_intent = stripe.PaymentIntent.create(
                #   amount=2500,
                #   currency='eur',
                #   setup_future_usage='off_session',
                #   customer=customer.id,
                #   payment_method_types=['sepa_debit'],
                #   # Verify your integration in this guide by including this parameter
                #   metadata={'integration_check': 'sepa_debit_accept_a_payment'},
                # )


                # stripe.WebhookEndpoint.create(
                #   url="https://prenota.cc/webhook/secret/stripe",
                #   enabled_events=[
                #     "payment_intent.succeeded",
                #     # "charge.succeeded",
                #   ],
                # )
                # print(customer, pay_intent, 'cazz')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

