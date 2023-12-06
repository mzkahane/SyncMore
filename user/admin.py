from django.contrib import admin

# Register your models here.
from .models import *


# Sign up Supervisor manager
class SupervisorManager(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_time', 'updated_time']
    list_display_links = ['name', 'is_active', 'created_time', 'updated_time']
    list_filter = ['name', 'is_active', 'created_time', 'updated_time']
    search_fields = ['name', 'is_active', 'created_time', 'updated_time']


# Sign up User manager
class UserManager(admin.ModelAdmin):
    list_display = ['First_Name', 'Last_Name', 'Username', 'password', 'address', 'gender', 'is_active', 'created_time',
                    'supervisor', 'updated_time', 'last_access_time', 'second_password']
    list_display_links = ['First_Name', 'Last_Name', 'Username', 'password', 'address', 'gender', 'is_active',
                          'created_time', 'supervisor', 'updated_time', 'last_access_time', 'second_password']
    list_filter = ['First_Name', 'Last_Name', 'Username', 'password', 'address', 'gender', 'is_active', 'created_time',
                   'supervisor', 'updated_time', 'last_access_time', 'second_password']
    search_fields = ['First_Name', 'Last_Name', 'Username', 'password', 'address', 'gender', 'is_active',
                     'created_time', 'supervisor', 'updated_time', 'last_access_time', 'second_password']


# Sign up Phone manager
class PhoneManager(admin.ModelAdmin):
    list_display = ['phone_user', 'phone', 'created_time', 'is_active', 'updated_time']
    list_display_links = ['phone_user', 'phone', 'created_time', 'is_active', 'updated_time']
    list_filter = ['phone_user', 'phone', 'created_time', 'is_active', 'updated_time']
    search_fields = ['phone_user', 'phone', 'created_time', 'is_active', 'updated_time']


# Sign up Note manager
class NoteManager(admin.ModelAdmin):
    list_display = ['note_user', 'title', 'content', 'created_time', 'is_active', 'updated_time']
    list_display_links = ['note_user', 'title', 'content', 'created_time', 'is_active', 'updated_time']
    list_filter = ['note_user', 'title', 'content', 'created_time', 'is_active', 'updated_time']
    search_fields = ['note_user', 'title', 'content', 'created_time', 'is_active', 'updated_time']


# Sign up Email manager
class EmailManager(admin.ModelAdmin):
    list_display = ['email_user', 'email', 'created_time', 'is_active', 'updated_time']
    list_display_links = ['email_user', 'email', 'created_time', 'is_active', 'updated_time']
    list_filter = ['email_user', 'email', 'created_time', 'is_active', 'updated_time']
    search_fields = ['email_user', 'email', 'created_time', 'is_active', 'updated_time']


# Sign up Document manager
class DocumentManager(admin.ModelAdmin):
    list_display = ['document_user', 'title', 'document', 'created_time', 'is_active', 'updated_time', 'issued_time',
                    'expired_time', 'type']
    list_display_links = ['document_user', 'title', 'document', 'created_time', 'is_active', 'updated_time',
                          'issued_time', 'expired_time', 'type']
    list_filter = ['document_user', 'title', 'document', 'created_time', 'is_active', 'updated_time', 'issued_time',
                   'expired_time', 'type']
    search_fields = ['document_user', 'title', 'document', 'created_time', 'is_active', 'updated_time', 'issued_time',
                     'expired_time', 'type']


# Register the Supervisor manager
admin.site.register(Supervisor, SupervisorManager)
# Register the User manager
admin.site.register(User, UserManager)
# Register the Phone manager
admin.site.register(Phone, PhoneManager)
# Register the Note manager
admin.site.register(Note, NoteManager)
# Register the Email manager
admin.site.register(Email, EmailManager)
# Register the Document manager
admin.site.register(Document, DocumentManager)

# Customize admin page style
admin.site.site_header = "SyncMore Admin System"
admin.site.site_title = "SyncMore Admin System"
admin.site.index_title = "Data Management"
