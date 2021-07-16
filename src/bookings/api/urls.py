from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingsAPIView.as_view()),
    path('shadow/', views.BookingsShadowAPIView.as_view()),
    path('notifications/', views.SendBookingNotificationView.as_view()),
    path('pay/shop/', views.BookingsPayFromShopAPIView.as_view()),
    path('week/<int:week>/', views.BookingsWeekAPIView.as_view()),
    path('week/<int:week>/external/', views.BookingsWeekExternalAPIView.as_view()),
    path('week/<int:week>/shop/', views.BookingsWeekByShopAPIView.as_view()),
    path('week/<int:week>/2shop/', views.Bookings2WeeksByShopAPIView.as_view()),
    path('week/<int:week>/5shop/', views.Bookings5WeeksByShopAPIView.as_view()),
    path('month/<int:month>/', views.BookingsMonthAPIView.as_view()),
    path('<int:pk>/', views.BookingsDetailAPIView.as_view()),
    path('user/', views.BookingsUserAPIView.as_view()),
    path('recurring/', views.BookRecurringAPIView.as_view()),
    path('recurring/delete/<int:pk>/', views.BookingsRecurringDeleteAPIView.as_view()),
    path('charts_data/', views.BookingsAggregateAPIView.as_view()),
    path('user/week/<int:week>/', views.BookingsUserWeekAPIView.as_view()),
    path('delete/shadow/', views.DeleteShadowsView.as_view()),
    # path('fast/asd/', views.FastUpdateView.as_view()),

]