from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClosedhoursAPIView.as_view()),
    path('<int:pk>/', views.ClosedhoursDetailAPIView.as_view()),
]