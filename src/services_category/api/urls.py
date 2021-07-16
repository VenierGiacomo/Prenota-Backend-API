from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ServiceCategoryAPIView.as_view()),

]