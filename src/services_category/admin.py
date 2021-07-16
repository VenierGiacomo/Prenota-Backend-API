from django.contrib import admin
from .models import ServiceCategory
# Register your models here.


class ServiceCategoryInterfaceAdmin(admin.ModelAdmin):
	list_display = ('id','shop', 'name')

admin.site.register(ServiceCategory,ServiceCategoryInterfaceAdmin)