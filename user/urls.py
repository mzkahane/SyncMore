from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_view),
    path('register', views.reg_view),
    path('logout', views.logout_view),
    path('index', views.index_view, name='index'),
    path('add_phone', views.add_phone),
    path('add_email', views.add_email),
    path('add_note', views.add_note),
    path('add_document', views.add_document),
    path('delete_phone/<int:phone_id>', views.delete_phone),
    path('delete_email/<int:email_id>', views.delete_email),
    path('delete_note/<int:note_id>', views.delete_note),
    path('delete_document/<int:document_id>', views.delete_document),
    path('modify_phone/<int:phone_id>', views.modify_phone),
    path('modify_email/<int:email_id>', views.modify_email),
    path('modify_note/<int:note_id>', views.modify_note),
    path('modify_document/<int:document_id>', views.modify_document),
    path('account', views.account),
    path('account_settings', views.account_settings),

]
