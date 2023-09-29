from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view),
    path('register', views.reg_view),
    path('logout', views.logout_view),
    path('index', views.index_view),
]
