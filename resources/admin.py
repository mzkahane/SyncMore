from django.contrib import admin

# Register your models here.
from .models import Resource


class ResourceManager(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    list_display_links = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    list_filter = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']
    search_fields = ['category', 'name', 'description', 'address', 'phone', 'email', 'website', 'website_nickname']


admin.site.register(Resource, ResourceManager)

admin.site.site_header = "Syncmore date system"
admin.site.site_title = "Syncmore date system"
admin.site.index_title = "Backend management"
