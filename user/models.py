from django.db import models


# Create your models here.
class User(models.Model):
    First_Name = models.CharField('First_Name', max_length=30, null=True)

    Last_Name = models.CharField('Last_Name', max_length=30, null=True)

    Username = models.CharField('Username', max_length=30)

    password = models.CharField('password', max_length=32)

    address = models.CharField('address', max_length=255, default="San Francisco", null=True)

    phone = models.IntegerField('phone', default=0000000000, null=True)

    gender = models.CharField('gender', max_length=6, default=None, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    email = models.CharField('email', max_length=30, default=None, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)
