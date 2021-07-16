"""calendarapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api.urls')),
    path('api/bookings/', include('bookings.api.urls')),
    path('api/store/', include('store.api.urls')),
    path('api/device/', include('userdevices.api.urls')),
    path('api/store/', include('store.api.urls')),
    path('api/addons/', include('addons.api.urls')),
    path('api/serviceaddons/', include('serviceaddons.api.urls')),
    path('api/services/', include('services.api.urls')),
    path('api/store/clients/', include('shopclients.api.urls')),
    path('api/closedhours/', include('closedhours.api.urls')),
    path('api/employees/', include('employees.api.urls')),
    path('api/email/', include('emailconfirmation.api.urls')),
    path('api/employeehours/', include('employeeshour.api.urls')),
    path('api/employee/services/', include('employeeservices.api.urls')),
    path('api/webhooks/', include('webhooks.api.urls')),
    path('api/customservices/', include('customservices.api.urls')),
    path('api/categories/', include('services_category.api.urls'))
]
