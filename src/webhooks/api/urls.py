
from django.urls import path
from . import views

urlpatterns = [
    path('portal/stripe', views.StripeCustomerPortalAPIView.as_view()),
    path('ticket', views.BusTriesteTicketAPIView.as_view()),
    path('activate_account/', views.StripeActivateConnect.as_view()),
    path('pay/business/', views.PayShopFromBooking.as_view()),
    path('pay/business/credits/', views.PayShopWithCreditBooking.as_view()),
    path('list/transactions', views.ListTransactionsAPIView.as_view()),
    path('payment_methods/', views.PaymentmethodsAPIView.as_view()),
    path('testnotifications/', views.selfNotificationsAPIView.as_view()),
    path('new_customer_socket/', views.newCustomeRequestAPIView.as_view()),
    # path('bus/applepay', views.BusApplePay.as_view()),
    path('session/stripe', views.StripeSessionAPIView.as_view()),
    path('prenota/stripe', views.StripeWeebhookAPIView.as_view()),
    # path('payment_intent', views.StripePayintentAPIView.as_view()),

]

