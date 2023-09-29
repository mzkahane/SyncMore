from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User
# Create your views here.
import hashlib
import sys
import re

sys.path.append('..')


def login_view(request):
    if request.method == 'GET':
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/user/index')
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/user/index')

        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(Username=username)
        except Exception as e:
            print('--login user error %s' % (e))
            note = 'username or password incorrect'
            dis = 'block'
            return render(request, 'user/login.html', locals())

        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            note = 'username or password incorrect'
            dis = 'block'
            return render(request, 'user/login.html', locals())

        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/user/index')

        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)

        return resp


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        if len(password_1) < 6:
            note = 'the length of password is too short, at least 6 letters'
            dis = 'block'
            return render(request, 'user/register.html', locals())

        if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", password_1):
            note = 'Failed, the password should include at least one digit, one uppercase and one lower case'
            dis = 'block'
            return render(request, 'user/register.html', locals())

        if password_1 != password_2:
            note = 'the two passwords are not match'
            dis = 'block'
            return render(request, 'user/register.html', locals())

        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        old_users = User.objects.filter(Username=username)
        if old_users:
            note = 'username has been signed up'
            dis = 'block'
            return render(request, 'user/register.html', locals())

        try:
            user = User.objects.create(Username=username, password=password_m)
        except Exception as e:
            print('--create user error %s' % (e))
            note = 'username has been signed up'
            dis = 'block'
            return render(request, 'user/register.html', locals())

        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/user/index')


def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('../')

    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp


def index_view(request):
    if request.method == 'GET':
        c_uid = request.COOKIES.get('uid')
        if c_uid is None:
            c_uid = request.session['uid']
    user = User.objects.filter(id=c_uid)
    return render(request, 'user/index.html', locals())
