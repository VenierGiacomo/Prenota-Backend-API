from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('', obtain_jwt_token),
    path('<int:pk>', views.DetailAccountAPIView.as_view()),
    path('register/', views.StdRegisterAPIView.as_view()),
    path('register/employee/', views.EmployeeRegisterAPIView.as_view()),
    path('refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='reset_password_template.html', html_email_template_name='email_template.html'), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent_template.html'), name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='change_passowrd_succes.html'), name="password_reset_complete"),
]