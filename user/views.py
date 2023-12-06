# Create your views here.
import hashlib
import re
import sys

import boto3
import requests
from botocore.exceptions import NoCredentialsError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from django.conf import settings
import boto3
from botocore.client import Config
from SyncMore import settings

from .forms import DocumentForm
from .models import Document, Email, Note, Phone, Supervisor, User
from django.contrib import messages

sys.path.append('..')


# This function is used to login
def login_view(request):
    # Display the page if getting a GET request
    if request.method == 'GET':
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/user/index')
        # Get the session
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/user/index')

        return render(request, 'user/login.html')
    # Handle the POST request if a user tries to login
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(Username=username)
        except Exception as e:
            print('--login user error %s' % (e))
            note = 'username or password incorrect'
            dis = 'block'
            messages.error(request, 'Username or password incorrect')

            return render(request, 'user/login.html', locals())

        # Encrypt the password
        m = hashlib.md5()
        m.update(password.encode())

        # If the password doesn't match
        if m.hexdigest() != user.password:
            note = 'username or password incorrect'
            dis = 'block'
            messages.error(request, 'Username or password incorrect')
            return render(request, 'user/login.html', locals())

        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/user/index')

        # Set up the session time
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)

        return resp


# This function is used to register for a new account
def reg_view(request):
    # Display the page if getting a GET request
    if request.method == 'GET':
        return render(request, 'user/register.html')
    # Handle the POST request if a user tries to sign up for a new account
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        second_password = request.POST['second_password']

        # Password restriction
        if len(password_1) < 6:
            note = 'the length of password is too short, at least 6 letters'
            dis = 'block'
            messages.error(request, 'The length of password is too short, at least 6 letters')
            return render(request, 'user/register.html', locals())

        if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", password_1):
            note = 'Failed, the password should include at least one digit, one uppercase and one lower case'
            dis = 'block'
            messages.error(request,
                           'Failed, the password should include at least one digit, one uppercase and one lower case')
            return render(request, 'user/register.html', locals())

        # If the two password don't match
        if password_1 != password_2:
            note = 'the two passwords are not match'
            dis = 'block'
            messages.error(request, 'The two passwords are not match')
            return render(request, 'user/register.html', locals())

        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        # If the username has been used
        old_users = User.objects.filter(Username=username)
        if old_users:
            note = 'username has been signed up'
            dis = 'block'
            messages.error(request, 'Username has been signed up')
            return render(request, 'user/register.html', locals())

        try:
            user = User.objects.create(Username=username, password=password_m, second_password=second_password)
        except Exception as e:
            print('--create user error %s' % (e))
            note = 'username has been signed up'
            dis = 'block'
            messages.error(request, 'Username has been signed up')
            return render(request, 'user/register.html', locals())

        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/user/index')


# This function is used to logout
def logout_view(request):
    # Get the session and clear it
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('../')
    # Get the COOKIES and clear it
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp


# This function is used to generate the authentication url to modify the object storage
def generate_presigned_url(object_name):
    s3_client = boto3.client('s3',
                             endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             config=Config(signature_version='s3v4'))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
        return response
    except Exception as e:
        print(e)
        return None  # Handle exceptions according to your needs


# This function is used to display the index view
def index_view(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']

    user = User.objects.get(id=c_uid)
    phones = Phone.objects.filter(phone_user_id=c_uid)
    emails = Email.objects.filter(email_user_id=c_uid)
    supervisor = Supervisor.objects.get(id=user.supervisor.id)
    notes = Note.objects.filter(note_user_id=c_uid)
    second_password = user.second_password

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        document_type = request.GET.get('type', None)
        documents = Document.objects.filter(document_user_id=c_uid,
                                            type=document_type) if document_type else Document.objects.filter(
            document_user_id=c_uid)

        # Generate the data passed to frontend
        documents_with_urls = []
        for document in documents:
            presigned_url = generate_presigned_url(
                document.document.name)
            documents_with_urls.append({
                'id': document.id,
                'title': document.title,
                'url': presigned_url
            })

        return JsonResponse({'documents': documents_with_urls}, safe=False)

    # If not an AJAX request, render the page normally with all the context
    document_type = request.GET.get('type', 'ID')
    documents = Document.objects.filter(document_user_id=c_uid, type=document_type)

    documents_with_urls = []
    for document in documents:
        presigned_url = generate_presigned_url(document.document.name)
        documents_with_urls.append({
            'id': document.id,
            'title': document.title,
            'url': presigned_url
        })
    # Generate the data passed to frontend
    context = {
        'user': user,
        'phones': phones,
        'emails': emails,
        'supervisor': supervisor,
        'notes': notes,
        'documents': documents_with_urls,
        'second_password': second_password
    }

    return render(request, 'user/index.html', context)


# This function is used to add the phone
def add_phone(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/add_phone.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        phone = request.POST.get('phone', "")
        Phone.objects.create(phone_user_id=c_uid, phone=phone)
        return HttpResponseRedirect('/user/index')


# This function is used to add the email
def add_email(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/add_email.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        email = request.POST.get('email', "")
        Email.objects.create(email_user_id=c_uid, email=email)
        return HttpResponseRedirect('/user/index')


# This function is used to add the note
def add_note(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/add_note.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        Note.objects.create(note_user_id=c_uid, title=title, content=content)
        return HttpResponseRedirect('/user/index')


# This function is used to add the document
def add_document(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # Display the page if getting a GET request
    if request.method == "GET":
        form = DocumentForm()
        # create dropdown options list and pass into render?
        return render(request, 'user/add_document.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        title = request.POST.get('title', "")
        document = request.FILES.get('document', "")
        type = request.POST.get('type', 'ID')
        Document.objects.create(document_user_id=c_uid, title=title, document=document, type=type)
        return HttpResponseRedirect('/user/index')


# This function is used to delete the phone
def delete_phone(request, phone_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        phone = Phone.objects.get(id=phone_id)
        phone.delete()
    return HttpResponseRedirect('/user/index')


# This function is used to modify the phone
def modify_phone(request, phone_id):
    phone = Phone.objects.get(id=phone_id)
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/modify_phone.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        phonee = request.POST.get('phone', "")
        phone.phone = phonee
        phone.save()
        return HttpResponseRedirect('/user/index')


# This function is used to delete the email
def delete_email(request, email_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        email = Email.objects.get(id=email_id)
        email.delete()
    return HttpResponseRedirect('/user/index')


# This function is used to modify the email
def modify_email(request, email_id):
    email = Email.objects.get(id=email_id)
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/modify_email.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        emaill = request.POST.get('email', "")
        email.email = emaill
        email.save()
        return HttpResponseRedirect('/user/index')


# This function is used to delete the note
def delete_note(request, note_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        note = Note.objects.get(id=note_id)
        note.delete()
    return HttpResponseRedirect('/user/index')


# This function is used to modify the note
def modify_note(request, note_id):
    note = Note.objects.get(id=note_id)
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/modify_note.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect('/user/index')


# This function is used to delete the document from the object storage
def delete_object_from_r2(object_name):
    delete_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{object_name}"
    headers = {
        "Authorization": f"Bearer {settings.R2_TOKEN}",
    }

    response = requests.delete(delete_url, headers=headers)
    return response.status_code == 200


# This function is used to delete the document
def delete_document(request, document_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        document = Document.objects.get(id=document_id)
        object_name = document.document.name
        if delete_object_from_r2(object_name):
            document.delete()
    return HttpResponseRedirect('/user/index')


# This function is used to modify the document
def modify_document(request, document_id):
    document = Document.objects.get(id=document_id)
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/modify_document.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        title = request.POST.get('title', "")
        documentt = request.FILES.get('document', document.document)
        document.title = title
        document.document = documentt
        document.save()
        return HttpResponseRedirect('/user/index')


# This function is used to display the user account information
def account(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    user = User.objects.get(id=c_uid)
    current_pin = user.second_password
    return render(request, 'user/account.html', locals())


# This function is used to modify the pin for the personal drive
def modify_second_password(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    user = User.objects.get(id=c_uid)
    # Save the new pin
    second_password = request.POST.get('second_password', "")
    user.second_password = second_password
    user.save()
    return HttpResponseRedirect('/user/index')
