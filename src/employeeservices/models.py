from django.db import models
from django.conf import settings
from store.models import Store
from services.models import ServicesStore
# Create your models here.

class EmployeeServices(models.Model):
    shop        = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    employee    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    service_id  = models.ForeignKey(ServicesStore, null=True, on_delete=models.CASCADE)
