from django.contrib import admin

# Register your models here.
from .models import Resource


# Sign up Resource manager
class ResourceManager(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    list_display_links = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    list_filter = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    search_fields = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']


# Register the Resource manager
admin.site.register(Resource, ResourceManager)

# Customize admin page style
admin.site.site_header = "SyncMore Admin System"
admin.site.site_title = "SyncMore Admin System"
admin.site.index_title = "Data Management"
