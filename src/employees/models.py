from django.db import models
from django.conf import settings
from store.models import Store
# Create your models here.

class Employee(models.Model):
    shop        = models.ForeignKey(Store, default=1, on_delete=models.CASCADE )
    employee    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE )
    name        = models.CharField(max_length=30)
    display     = models.BooleanField(default=True)


