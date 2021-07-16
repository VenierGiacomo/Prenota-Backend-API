from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomServicesAPIView.as_view()),
    path('<int:pk>/', views.CustomServicesDetailAPIView.as_view()),

]