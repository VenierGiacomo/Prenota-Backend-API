from django.contrib import admin
from .models import UserDevice
# Register your models here.

class UserDeviceInterfaceAdmin(admin.ModelAdmin):
	list_display = ('user','id')
	search_fields = ('user',)



admin.site.register(UserDevice,UserDeviceInterfaceAdmin)



