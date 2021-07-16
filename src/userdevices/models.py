from django.db import models
from django.conf import settings
# Create your models here.

class UserDevice(models.Model):

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL )
    player_id   = models.CharField(max_length=150)


