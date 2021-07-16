from django.urls import path
from . import views

urlpatterns = [
    path('store/all', views.StoreAddOnsAPIView.as_view()),
    path('<int:service_id>', views.ServiceAddOnsAPIView.as_view()),


]

