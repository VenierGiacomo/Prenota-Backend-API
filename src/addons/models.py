from django.db import models
from store.models import Store
# Create your models here.

class AddOn(models.Model):
    name             = models.TextField(null=True, blank=True)
    shop             = models.ForeignKey(Store, default=1, on_delete=models.CASCADE )
    price            = models.IntegerField()
    duration         = models.IntegerField()
    description      = models.TextField(null=True, blank=True)
    id_c             = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.shop.store_name +' - ' + self.name + ' - ' + str(self.id)

    def save(self, *args, **kwargs):
        if self.id_c is None:
            self.id_c = 0 + self.id
        super().save(*args, **kwargs)
# Create your models here.
