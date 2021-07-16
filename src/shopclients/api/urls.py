from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreClientsAPIView.as_view()),
    path('QRCode', views.StoreClientsByQRCodeAPIView.as_view()),
    path('<int:pk>/', views.StoreClientsDetailAPIView.as_view()),
    path('is/', views.IsStoreClientsAPIView.as_view()),
    path('new/', views.StoreClientsNewAPIView.as_view()),
     path('invite/email/', views.StoreClientsInviteEmailAPIView.as_view()),


]

