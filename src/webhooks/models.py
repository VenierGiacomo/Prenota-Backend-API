from django.db import models

# Create your models here.

class StripeData(models.Model):
    hook_type        = models.TextField(null=True, blank=True)
    data_string      = models.TextField(null=True, blank=True)
    client           = models.TextField(null=True, blank=True)
    time_stamp	= models.DateTimeField(auto_now_add=True,  null=True, blank=True)

# Create your models here.
