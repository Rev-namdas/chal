from django.db import models

# Create your models here.
class stockModel(models.Model):
    stockedby = models.CharField(max_length=30)
    rice = models.CharField(max_length=30)
    amount = models.IntegerField()
    bosta = models.IntegerField()
    time = models.DateTimeField(default="")


class sellStockModel(models.Model):
    customer = models.CharField(max_length=30)
    rice = models.CharField(max_length=30)
    amount = models.IntegerField()
    bosta = models.IntegerField()
    time = models.DateTimeField(default="")
    price = models.IntegerField()


class productsModel(models.Model):
    product = models.CharField(max_length=30)
    productamount = models.IntegerField(default=0, blank=True)
    productbosta = models.IntegerField(default=0, blank=True)


class remainingModel(models.Model):
    product     = models.CharField(max_length=30, default="")
    ramount     = models.IntegerField(default=0)
    rbosta      = models.IntegerField(default=0)