from datetime import date

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create a Supervisor table in the database
class Supervisor(models.Model):
    name = models.CharField('name', max_length=50, default='Zac Clark')

    position = models.CharField('position', max_length=50, default='Team Leader')

    email = models.CharField('email', max_length=50, default='zac@homemoreproject.org', null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


# Create a UserManger table in the database for the admin system
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and save a regular User with the given username and password.
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        user = self.model(Username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(Username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(Username=username)


# Create your models here.

# Create a User table in the database
class User(AbstractBaseUser, PermissionsMixin):
    First_Name = models.CharField('First_Name', max_length=30, null=True)

    Last_Name = models.CharField('Last_Name', max_length=30, null=True)

    Username = models.CharField('Username', max_length=30, unique=True)

    password = models.CharField('password', max_length=128)

    address = models.CharField('address', max_length=255, default="San Francisco", null=True)

    gender = models.CharField('gender', max_length=6, default=None, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, default=1, related_name='supervisor')

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)

    last_access_time = models.DateTimeField('last_access_time', auto_now_add=True, null=True)

    second_password = models.IntegerField('second_password', null=True)

    objects = UserManager()

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'Username'

    REQUIRED_FIELDS = ['First_Name', 'Last_Name']


# Create a Phone table in the database
class Phone(models.Model):
    phone_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_user')

    phone = models.IntegerField('phone', default=00000000000000000000, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


# Create a Note table in the database
class Note(models.Model):
    note_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_user')

    title = models.CharField('title', max_length=32)

    content = models.TextField('content')

    created_time = models.DateField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateField('updated_time', auto_now_add=True, null=True)


# Create a Email table in the database
class Email(models.Model):
    email_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_user')

    email = models.CharField('email', max_length=30, default=None, null=True)

    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateTimeField('updated_time', auto_now_add=True, null=True)


# Create a Document table in the database
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

    created_time = models.DateField('created_time', auto_now_add=True, null=True)

    is_active = models.BooleanField('is_active', default=True, null=True)

    updated_time = models.DateField('updated_time', auto_now_add=True, null=True)

    issued_time = models.DateField('issued_time', auto_now_add=True, null=True)

    expired_time = models.DateField('expired_time', auto_now=False, auto_now_add=False, null=True)

    type = models.CharField('type', max_length=32, default='Other', null=True, choices=TYPE_CHOICES)
