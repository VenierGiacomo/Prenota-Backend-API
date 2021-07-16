from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServicesStoreAPIView.as_view()),
    path('byshop/', views.ServicesStoreByShopAPIView.as_view()),
    path('<int:pk>/', views.ServicesStoreDetailAPIView.as_view()),
    # path('setdefault',views.ServicesStoreDefaultAllAPIView.as_view()),
]