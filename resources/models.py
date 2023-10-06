from django.db import models


# Create your models here.
class Resource(models.Model):
    category = models.CharField('category', max_length=128, null=True)
    name = models.CharField('name', max_length=128)
    description = models.CharField('description', max_length=1024, null=True)
    address = models.CharField('address', max_length=128, null=True)
    phone = models.CharField('phone', max_length=16, null=True)
    email = models.EmailField('email', max_length=30, null=True)
    website = models.CharField('website', max_length=50, null=True)
    website_nickname = models.CharField('website_nickname', max_length=50, null=True)
