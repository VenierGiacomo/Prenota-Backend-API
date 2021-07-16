from django.contrib import admin
from .models import ServicesStore
# Register your models here.


class ServicesStoreInterfaceAdmin(admin.ModelAdmin):
	list_display = ('shop','name','id')
	search_fields = ('shop','name')



admin.site.register(ServicesStore,ServicesStoreInterfaceAdmin)