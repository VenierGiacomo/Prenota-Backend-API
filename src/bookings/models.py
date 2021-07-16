from django.db import models
from django.conf import settings
from store.models import Store
# Create your models here.

class Bookings(models.Model):
    shop        = models.ForeignKey(Store, default=1, on_delete=models.SET_DEFAULT )
    client      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client', null=True, on_delete=models.SET_NULL )
    employee    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='booking_employee', null=True, on_delete=models.SET_NULL )
    start       = models.IntegerField()
    end         = models.IntegerField()
    start_t     = models.IntegerField(null=True, blank=True)
    end_t       = models.IntegerField(null=True, blank=True)
    day         = models.IntegerField()
    week        = models.IntegerField()
    month       = models.IntegerField()
    year        = models.IntegerField()
    phone       = models.TextField(null=True, blank=True)
    store_name       = models.TextField(null=True, blank=True)
    store_phone       = models.TextField(null=True, blank=True)
    client_name = models.TextField()
    location = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    booked_at	= models.DateTimeField(verbose_name='last login', auto_now_add=True,  null=True, blank=True)
    note        = models.TextField(null=True, blank=True)
    details     = models.TextField(null=True, blank=True)
    service_n   = models.TextField(null=True, blank=True)
    recurring_id = models.IntegerField(null=True, blank=True)
    payed = models.BooleanField(default=False)
    booked_on_plt = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    day_to_delete = models.IntegerField(default=2)
    visible = models.BooleanField(default=True)
    store_client = models.IntegerField(default=1)

    def __str__(self):
        return str(self.store_name+" "+ str(self.id) +" "+str(self.client) )

# Create your models here.
