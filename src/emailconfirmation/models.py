from django.db import models
from django.conf import settings
# Create your models here.

class Emailconfirmation(models.Model):
        email = models.CharField(max_length=50)
        name = models.CharField(max_length=50)
        surname = models.CharField(max_length=50)
        day = models.IntegerField()
        month = models.CharField(max_length=50)
        year = models.IntegerField()
        time = models.CharField(max_length=50)
        service = models.CharField(max_length=100)
        shop = models.CharField(max_length=50)

class Registerconfirmation(models.Model):
        name = models.CharField(max_length=50)
        surname = models.CharField(max_length=50)
        email = models.CharField(max_length=50)
        phone = models.CharField(max_length=50)
