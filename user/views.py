# Create your views here.
import hashlib
import re
import sys
from datetime import datetime

import boto3
import requests
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from SyncMore import settings

from .forms import DocumentForm
from .models import Document, Email, Note, Phone, Supervisor, User

sys.path.append('..')

TIME_ZONE = 'America/Los_Angeles'


# Handles User Login page functionality
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
            note = 'Username or password is incorrect.'
            dis = 'block'
            messages.error(request, 'Username or password is incorrect.')

            return render(request, 'user/login.html', locals())

        # Encrypt the password
        m = hashlib.md5()
        m.update(password.encode())

        # If the password doesn't match
        if m.hexdigest() != user.password:
            note = 'Username or password is incorrect.'
            dis = 'block'
            messages.error(request, 'Username or password is incorrect.')
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

        # Password length restriction
        if len(password_1) < 6:
            note = 'the length of password is too short, at least 6 letters'
            dis = 'block'
            messages.error(request, 'The length of password is too short, at least 6 letters')
            return render(request, 'user/register.html', locals())
        # check if given password meets the requirements
        if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", password_1):
            note = 'Failed, the password should include at least one digit, one uppercase and one lower case'
            dis = 'block'
            messages.error(request,
                           'Failed, the password should include at least one digit, one uppercase and one lower case')
            return render(request, 'user/register.html', locals())

        # If the entered password and retyped password don't match
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

        # attempt to create a new user--check if username is unique
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
    # get the user by their UID, and all objects which belong to the user by their UID
    user = User.objects.get(id=c_uid)
    phones = Phone.objects.filter(phone_user_id=c_uid)
    emails = Email.objects.filter(email_user_id=c_uid)
    supervisor = Supervisor.objects.get(id=user.supervisor.id)
    notes = Note.objects.filter(note_user_id=c_uid)
    second_password = user.second_password
    documents = Document.objects.filter(document_user_id=c_uid)

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
                'type': document.type,
                'id': document.id,
                'title': document.title,
                'url': presigned_url
            })

        return JsonResponse({'documents': documents_with_urls}, safe=False)
    # Generate the data passed to frontend
    context = {
        'user': user,
        'phones': phones,
        'emails': emails,
        'supervisor': supervisor,
        'notes': notes,
        'documents': documents,
        'second_password': second_password
    }

    return render(request, 'user/index.html', context)


# Function which handles the updating user info functionality from the User Home Page
# when user is editing First Name, Last Name, and Description of current living area
def add_user_info(request):
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # get the user by their UID and their respective information
    user = User.objects.get(id=c_uid)
    first_name = user.First_Name
    last_name = user.Last_Name
    living_area = user.address
    new_first_name = request.POST.get('new_first_name', "")
    new_last_name = request.POST.get('new_last_name', "")
    new_living_area = request.POST.get('new_living_area', "")

    # if the user's first name has been updated
    if first_name != new_first_name:
        user.First_Name = new_first_name

    # if the user's last name has been updated
    if last_name != new_last_name:
        user.Last_Name = new_last_name

    # if the user's description of living area has been updated
    if living_area != new_living_area:
        user.address = new_living_area

    # save changes to user
    user.save()
    return HttpResponseRedirect('/user/index')


# This function handles the user functionality to a new phone number
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


# This function handles the user functionality to add a new email
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


# This function handles the user functionality to add a new note
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


# This function handles the user functionality to add a new document
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
        type = request.POST.get('type', 'Other')
        date_str = request.POST.get('expiration-date', "")
        expiration_date = parse_date(date_str)
        # Allowed file types
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
        # Check if the file is of an allowed type
        if any(document.name.lower().endswith(ext) for ext in allowed_extensions):
            Document.objects.create(document_user_id=c_uid, title=title, document=document, type=type,
                                    expired_time=expiration_date)
            return HttpResponseRedirect('/user/index')
        else:
            messages.error(request, 'Invalid file type. Allowed types are: PNG, JPG, JPEG, PDF.')
    return HttpResponseRedirect('/user/add_document')


# This function handles the user functionality to delete a phone number
def delete_phone(request, phone_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        phone = Phone.objects.get(id=phone_id)
        phone.delete()
    return HttpResponseRedirect('/user/index')


# This function handles the user functionality to modify a phone number
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


# This function handles the user functionality to delete an email
def delete_email(request, email_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        email = Email.objects.get(id=email_id)
        email.delete()
    return HttpResponseRedirect('/user/index')


# This function handles the user functionality to modify an email
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


# This function handles the user functionality to delete a note
def delete_note(request, note_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        note = Note.objects.get(id=note_id)
        note.delete()
    return HttpResponseRedirect('/user/index')


# This function handles the user functionality to modify a note
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
        # update the notes updated time to the current time
        note.updated_time = datetime.now()
        note.save()
        return HttpResponseRedirect('/user/index')


# This function is used to delete the document from the object storage
def delete_object_from_r2(object_name):
    r2_endpoint_url = settings.AWS_S3_ENDPOINT_URL
    client = boto3.client('s3',
                          endpoint_url=r2_endpoint_url,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_name)


# This function handles the user functionality to delete a document
def delete_document(request, document_id):
    # Make changes to the database if getting a POST request
    if request.method == "POST":
        document = Document.objects.get(id=document_id)
        object_name = document.document.name
        delete_object_from_r2(object_name)
        document.delete()
    return HttpResponseRedirect('/user/index')


# This function handles the user functionality to modify a document
def modify_document(request, document_id):
    document = Document.objects.get(id=document_id)
    # Display the page if getting a GET request
    if request.method == "GET":
        return render(request, 'user/modify_document.html', locals())
    # Make changes to the database if getting a POST request
    elif request.method == "POST":
        title = request.POST.get('title', "")
        delete_object_from_r2(document.document.name)
        new_document = request.FILES.get('document', document.document)

        # Allowed file types
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
        if any(new_document.name.lower().endswith(ext) for ext in allowed_extensions):
            document.document = new_document
        else:
            # Add error message for invalid file type
            messages.error(request, 'Invalid file type. Allowed types are: PNG, JPG, JPEG, PDF.')
            return HttpResponseRedirect('user/modify_document/' + document)

        document.title = title
        document.updated_time = datetime.now()
        # update the document type, if one is provided
        type = request.POST.get('type', "")
        if type != 'Unchanged':
            document.type = type
        # update the document expiration date, if one is provided
        date_str = request.POST.get('expiration-date', "")
        if date_str != None:
            expiration_date = parse_date(date_str)
            document.expired_time = expiration_date
        # save document changes
        document.save()
        return HttpResponseRedirect('/user/index')


# This function is used to display the user account information
def account(request):
    # Get the session
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    user = User.objects.get(id=c_uid)
    username = user.Username
    password = user.password
    current_pin = user.second_password
    return render(request, 'user/account.html', locals())


# This function handles the user functionality to modify user account information
# user account information involves: username, password, and 4-digit PIN
def account_settings(request):
    c_uid = request.COOKIES.get('uid')
    if c_uid is None:
        c_uid = request.session['uid']
    # get the user by their UID and respective account information
    user = User.objects.get(id=c_uid)
    username = user.Username
    password = user.password
    current_pin = user.second_password
    new_username = request.POST.get('new_username', "")
    new_password = request.POST.get('new_password', "")
    new_password_retype = request.POST.get('new_password_retype', "")
    new_second_password = request.POST.get('second_password', "")

    # if the username has been updated
    if user.Username != new_username:
        old_users = User.objects.filter(Username=new_username)
        if old_users:
            note = 'Username is taken already! Please try a different one.'
            dis = 'block'
            return render(request, 'user/account.html', locals())
        # if all checks passed, update username with new username
        else:
            user.Username = new_username

    # if the password has been updated
    if new_password:
        # check if the length of the password meets requirements
        if len(new_password) < 6:
            note = 'The length of the new password is too short. Password must be at least 6 characters.'
            dis = 'block'
            return render(request, 'user/account.html', locals())
        # check if the password meets other requirements
        if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", new_password):
            note = 'The new password does not meet the requirements. Password should include at least one digit, one uppercase letter, and one lowercase letter.'
            dis = 'block'
            return render(request, 'user/account.html', locals())
        # check that the entered password and retyped password match
        if new_password != new_password_retype:
            note = 'The new password does not match the retyped new password.'
            dis = 'block'
            return render(request, 'user/account.html', locals())

        m = hashlib.md5()
        m.update(new_password.encode())
        password_m = m.hexdigest()
        # if all checks passed, update user password with new one
        user.password = password_m

    # if user pin has been updated
    if new_second_password != user.second_password:
        if len(new_second_password) != 4:
            note = 'The length of the PIN must be 4 digits.'
            dis = 'block'
            return render(request, 'user/account.html', locals())

        if not re.search("^\d{4}$", new_second_password):
            note = 'The PIN must be exactly 4 digits.'
            dis = 'block'
            return render(request, 'user/account.html', locals())
        # if all checks passed, update user PIN with new PIN
        user.second_password = new_second_password

    # save changes to user
    user.save()
    return HttpResponseRedirect('/user/index')


def redirect_to_home(request, exception):
    return HttpResponseRedirect('/')
