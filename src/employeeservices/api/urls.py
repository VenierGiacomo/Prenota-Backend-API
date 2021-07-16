from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeServicesAPIView.as_view()),
    path('store/', views.EmployeeServicesfromStoreAPIView.as_view()),
    path('<int:employee>/<int:service>/', views.EmployeeServicesdetatilAPIView.as_view()),
]