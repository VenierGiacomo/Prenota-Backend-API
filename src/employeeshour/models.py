from django.db import models
from django.conf import settings
from store.models import Store
# Create your models here.

class Employeeshour(models.Model):
    shop        = models.ForeignKey(Store, null=True, on_delete=models.CASCADE )
    employee    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    wkday       = models.IntegerField() #1 = Monday #2 = Tuesday ecc
    start       = models.IntegerField() #0 = 07:00 , 1 = 07:05 , 12 = 08:00
    end         = models.IntegerField()
    start_t     = models.IntegerField(null=True, blank=True) #0 = 07:00 , 1 = 07:05 , 12 = 08:00
    end_t       = models.IntegerField(null=True, blank=True)

    #0 = 07:00 , 1 = 07:05 , 12 = 08:00

    def __str__(self):
        return str(self.shop.store_name)