from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views as resources_view

urlpatterns = [
    path("index", resources_view.resources_view),
    path('edit', resources_view.edit_resources),
    path('delete/<int:resource_id>', resources_view.delete),
    path('modify/<int:resource_id>', resources_view.modify),
    path('add', resources_view.add),
]
