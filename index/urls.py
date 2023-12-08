from django.contrib import admin
from django.urls import include, path

from . import views as index_view

urlpatterns = [
    # index/contact/ maps the contact_view to the Contact Us page
    path("contact/", index_view.contact_view, name='contact'),
]
