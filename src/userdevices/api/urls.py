from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceAPIView.as_view()),
]