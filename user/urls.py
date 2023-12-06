from django.urls import path
from . import views

urlpatterns = [
    # /user/login
    path('login', views.login_view),
    # /user/register
    path('register', views.reg_view),
    # /user/logout
    path('logout', views.logout_view),
    # /user/index
    path('index', views.index_view, name='index'),
    # /user/add_phone
    path('add_phone', views.add_phone),
    # /user/add_email
    path('add_email', views.add_email),
    # /user/add_note
    path('add_note', views.add_note),
    # /user/add_document
    path('add_document', views.add_document),
    # /user/delete_phone/<int:phone_id>
    path('delete_phone/<int:phone_id>', views.delete_phone),
    # /user/delete_email/<int:email_id>
    path('delete_email/<int:email_id>', views.delete_email),
    # /user/delete_note/<int:note_id>
    path('delete_note/<int:note_id>', views.delete_note),
    # /user/delete_document/<int:document_id>
    path('delete_document/<int:document_id>', views.delete_document),
    # /user/modify_phone/<int:phone_id>
    path('modify_phone/<int:phone_id>', views.modify_phone),
    # /user/modify_email/<int:email_id>
    path('modify_email/<int:email_id>', views.modify_email),
    # /user/modify_note/<int:note_id>
    path('modify_note/<int:note_id>', views.modify_note),
    # /user/modify_document/<int:document_id>
    path('modify_document/<int:document_id>', views.modify_document),
    # /user/account
    path('account', views.account),
    # /user/modify_second_password
    path('modify_second_password', views.modify_second_password),

]
