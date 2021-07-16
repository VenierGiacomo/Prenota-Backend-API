from django.db import models
from store.models import Store
from services.models import ServicesStore
from shopclients.models import StoreClient

# Create your models her


class CustomService(models.Model):
    shop             = models.ForeignKey(Store, default=1, on_delete=models.CASCADE )
    service          = models.ForeignKey(ServicesStore, on_delete=models.CASCADE)
    store_client     = models.ForeignKey(StoreClient, on_delete=models.CASCADE)
    duration         = models.IntegerField()
    price            = models.IntegerField()

    def __str__(self):
        return self.shop.store_name +' - ' + self.service.name + ' - ' + self.store_client.client_name

# Create your models here.
