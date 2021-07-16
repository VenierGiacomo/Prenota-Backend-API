from django.urls import path
from . import views

urlpatterns = [
    path('bookingconfirm', views.ConfirmBookingsAPIView.as_view()),
    path('registrationconfirm', views.ConfirmRegistrationAPIView.as_view()),

]