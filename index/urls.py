from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views as index_view

urlpatterns = [
    # index/contact/
    path("contact/", index_view.contact_view, name='contact'),
]
