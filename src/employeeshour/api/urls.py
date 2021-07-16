from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeehoursAPIView.as_view()),
    path('shop/', views.EmployeehoursByShopAPIView.as_view()),
    path('<int:pk>/', views.EmployeehoursDetailAPIView.as_view()),
]