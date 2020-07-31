
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

class Receipts(models.Model):
    Date =models.DateField(default=timezone.now)
    Memfees=models.IntegerField()
    Fines=models.IntegerField()
    Interests=models.IntegerField()
    Principal=models.IntegerField()
    Openingbal=models.IntegerField()
    Rmkfunds=models.IntegerField()
    RegIMO=models.CharField(max_length=10,default="")
    Micellaneous = models.IntegerField(default=0)

class Payments(models.Model):
    Shgloans=models.IntegerField()
    Feesandcharges=models.IntegerField()
    Salaries=models.IntegerField()
    Adminexpenses=models.IntegerField()
    Stationery=models.IntegerField()
    Micellaneous=models.IntegerField()
    Closingbal=models.IntegerField()
    RegIMO=models.CharField(max_length=10,default="")

class Account(models.Model):
    Field=models.CharField(max_length=15)
    RandP=models.CharField(max_length=10)
    IandE=models.CharField(max_length=10)
    BalSheet=models.CharField(max_length=10)
    Amount=models.IntegerField(default=0)