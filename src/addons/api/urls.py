from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddonsAPIView.as_view()),
]
