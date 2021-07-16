from django.db import models
from services.models import ServicesStore
from addons.models import AddOn
from store.models import Store
# Create your models here.

class ServiceAddOn(models.Model):
    service_id  = models.ForeignKey(ServicesStore, on_delete=models.CASCADE)
    addon_id    = models.ForeignKey(AddOn, on_delete=models.CASCADE )
    shop_id     = models.ForeignKey(Store,  on_delete=models.CASCADE )
