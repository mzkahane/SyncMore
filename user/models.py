from datetime import date

from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Supervisor(models.Model):
    name = models.CharField('name', max_length=30, default='Zac')

    is_active = models.BooleanField('is_active', default=True, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


# Create your models here.
class User(models.Model):
    First_Name = models.CharField('First_Name', max_length=30, null=True)

    Last_Name = models.CharField('Last_Name', max_length=30, null=True)

    Username = models.CharField('Username', max_length=30)

    password = models.CharField('password', max_length=32)

    address = models.CharField('address', max_length=255, default="San Francisco", null=True)

    gender = models.CharField('gender', max_length=6, default=None, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, default=1, related_name='supervisor')

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)

    last_access_time = models.DateTimeField('last_access_time', auto_now_add=True, null=True)

    second_password = models.IntegerField('second_password', null=True)


class Phone(models.Model):
    phone_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_user')

    phone = models.IntegerField('phone', default=0000000000, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


class Note(models.Model):
    note_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_user')

    title = models.CharField('title', max_length=32)

    content = models.TextField('content')

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


class Email(models.Model):
    email_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_user')

    email = models.CharField('email', max_length=30, default=None, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


class Document(models.Model):
    TYPE_CHOICES = [
        ('Other', 'Other'),
        ('ID', 'ID'),
        ('Passport', 'Passport'),
        ('SSN', 'SSN'),
        ('Birth Certificate', 'Birth Certificate'),
        ('Housing', 'Housing'),
        ('Financial', 'Financial'),
        ('Insurance', 'Insurance')
    ]
    document_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_user')

    title = models.CharField('title', max_length=32)

    document = models.FileField('document', storage=S3Boto3Storage())

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)

    issued_time = models.DateTimeField('issued_time', auto_now_add=True, null=True)

    expired_time = models.DateField('expired_time', auto_now=False, auto_now_add=False, blank=True, null=True)

    type = models.CharField('type', max_length=32, default='Other', null=True, choices=TYPE_CHOICES)
