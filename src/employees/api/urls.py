from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeesAPIView.as_view()),
    path('store/', views.EmployeeDetailAPIView.as_view()),
    path('delete/<int:pk>/', views.EmployeeDeleteAPIView.as_view()),
]