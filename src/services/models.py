from django.db import models
from django.conf import settings
from store.models import Store
from services_category.models import ServiceCategory

# Create your models here.

class ServicesStore(models.Model):
    shop        = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    duration    = models.IntegerField() #1 = Monday #2 = Tuesday ecc
    duration_book = models.IntegerField(null=True)
    sex         = models.IntegerField() #0 = 07:00 , 1 = 07:05 , 12 = 08:00
    max_n       = models.IntegerField() #0 = 07:00 , 1 = 07:05 , 12 = 08:00
    color       = models.IntegerField()
    price       = models.IntegerField()
    price_2     = models.IntegerField(null=True, blank=True)
    category    = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    favorite    = models.BooleanField(default=True)
    display     = models.BooleanField(default=True)
    hasToBeMember     = models.BooleanField(default=False)
    hasToBeCLient     = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.duration_book is None:
            self.duration_book = 0 + self.duration
        if self.price_2 is None:
            self.price_2 = 0 + self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop.store_name +' - ' +self.name