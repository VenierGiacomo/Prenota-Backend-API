from django.db import models
from django.conf import settings
from store.models import Store
# Create your models here.

class StoreClient(models.Model):
    shop                 = models.ForeignKey(Store, default=1, on_delete=models.SET_DEFAULT )
    client_name          = models.TextField()
    client               = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL )
    phone                = models.TextField(null=True, blank=True)
    email                = models.TextField(null=True, blank=True)
    credit               = models.IntegerField(default=0)
    note                 = models.TextField(default='', null=True, blank=True)
    isMember             = models.BooleanField(default=False)

    def __str__(self):
        return self.shop.store_name +' - ' +self.client_name


# Create your models here.
