from django.contrib import admin
from .models import Bookings
# Register your models here.


class BookingInterfaceAdmin(admin.ModelAdmin):
	list_display = ('client_name','store_name', 'visible', 'id','payed', 'booked_on_plt','booked_at')
	search_fields = ('client_name','store_name','id')



admin.site.register(Bookings,BookingInterfaceAdmin)