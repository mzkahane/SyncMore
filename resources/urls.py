from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views as resources_view

urlpatterns = [
    path("index", resources_view.resources_view),
]
