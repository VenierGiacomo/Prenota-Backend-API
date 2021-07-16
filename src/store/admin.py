from django.contrib import admin

from .models import Store
# Register your models here.


class StoreInterfaceAdmin(admin.ModelAdmin):
	list_display = ('store_name', 'id','payable','credits','stripe_connect', )
	search_fields = ('store_name',)



admin.site.register(Store,StoreInterfaceAdmin)
