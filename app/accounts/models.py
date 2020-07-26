
from django.db import models
from django.utils import timezone

# Create your models here.
class ledger(models.Model):
    Date = models.DateField(default=timezone.now)
    AccountName=models.CharField(max_length=20)
    TransctionType=models.CharField(max_length=50)
    Particulars=models.CharField(max_length=20)
    Amount=models.IntegerField()
    RegIMO=models.CharField(max_length=10,default="")
