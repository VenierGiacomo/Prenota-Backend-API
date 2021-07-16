from django.contrib import admin
from .models import StoreClient
# Register your models here.


class StoreClientInterfaceAdmin(admin.ModelAdmin):
	list_display = ('client_name','shop','id')
	search_fields = ('client_name',)



admin.site.register(StoreClient,StoreClientInterfaceAdmin)



