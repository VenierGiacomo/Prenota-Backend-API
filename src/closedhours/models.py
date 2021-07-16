from django.db import models

from store.models import Store
# Create your models here.

class Closedhours(models.Model):
    shop        = models.ForeignKey(Store, default=1, on_delete=models.SET_DEFAULT )
    wkday       = models.IntegerField() #1 = Monday #2 = Tuesday ecc
    start       = models.IntegerField() #0 = 07:00 , 1 = 07:05 , 12 = 08:00 
    end         = models.IntegerField() #1 = 5 minutes

