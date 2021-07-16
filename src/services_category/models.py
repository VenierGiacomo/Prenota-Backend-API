from django.db import models
from store.models import Store
# Create your models here.

class ServiceCategory(models.Model):
    name             = models.TextField(null=True, blank=True)
    shop             = models.ForeignKey(Store, default=1, on_delete=models.CASCADE )


    def __str__(self):
        return self.shop.store_name +' - ' + self.name

