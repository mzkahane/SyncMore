from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


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


class Phone(models.Model):
    phone_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_user')

    phone = models.IntegerField('phone', default=0000000000, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)


class Note(models.Model):
    note_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_user')

    title = models.CharField('title', max_length=32)

    content = models.TextField('content')

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)


class Email(models.Model):
    email_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_user')

    email = models.CharField('email', max_length=30, default=None, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)


class Supervisor(models.Model):
    supervisor_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor_user')

    name = models.CharField('name', max_length=30)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)


class Document(models.Model):
    document_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_user')

    title = models.CharField('title', max_length=32)

    # document = models.FileField('document', upload_to='documents', default=False)
    document = models.FileField('document', storage=S3Boto3Storage())

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)
