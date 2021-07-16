from django.contrib import admin
from .models import AddOn
# Register your models here.


# class BookingInterfaceAdmin(BookingsAdmin):
# 	list_display = ('email','date_joined', 'last_login', 'id','is_staff')



admin.site.register(AddOn)