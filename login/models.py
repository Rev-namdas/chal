from django.db import models

# Create your models here.
class loginModel(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    time = models.CharField(max_length=30, default="")


class AdminPassword(models.Model):
    admin_password = models.CharField(max_length=30)