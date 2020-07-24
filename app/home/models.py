from django.db import models


# Create your models here.

class register(models.Model):
    objects = models.Manager()
    nmo = models.CharField(max_length=40)
    headname = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    phno = models.IntegerField()
    uniqueid = models.IntegerField()
    password = models.CharField(max_length=20)
