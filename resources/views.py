from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Resource
from django.core.paginator import Paginator
import resources


# Create your views here.
def resources_view(request):
    resources = Resource.objects.all().order_by('category')
    page_num = request.GET.get('page', 1)
    paginator = Paginator(resources, 10)
    c_page = paginator.page(int(page_num))
    return render(request, 'resources/resources.html', locals())


def edit_resources(request):
    if request.method == "GET":
        resources = Resource.objects.all().order_by('category')
        return render(request, 'resources/edit.html', locals())


def delete(request, resource_id):
    if request.method == "POST":
        resource = Resource.objects.get(id=resource_id)
        resource.delete()
    return HttpResponseRedirect('/resources/edit')


def modify(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    if request.method == "GET":
        return render(request, 'resources/modify.html', locals())
    elif request.method == "POST":
        category = request.POST.get('category', "")
        name = request.POST.get('name', "")
        description = request.POST.get('description', "")
        address = request.POST.get('address', "")
        phone = request.POST.get('phone', "")
        email = request.POST.get('email', "")
        website = request.POST.get('website', "")
        website_nickname = request.POST.get('website_nickname', "")
        resource.category = category
        resource.name = name
        resource.description = description
        resource.address = address
        resource.phone = phone
        resource.email = email
        resource.website = website
        resource.website_nickname = website_nickname
        resource.save()
        return HttpResponseRedirect('/resources/edit')


def add(request):
    if request.method == "GET":
        return render(request, 'resources/add.html', locals())
    elif request.method == "POST":
        category = request.POST.get('category', "")
        name = request.POST.get('name', "")
        description = request.POST.get('description', "")
        address = request.POST.get('address', "")
        phone = request.POST.get('phone', "")
        email = request.POST.get('email', "")
        website = request.POST.get('website', "")
        website_nickname = request.POST.get('website_nickname', "link")
        Resource.objects.create(category=category, name=name, description=description, address=address, phone=phone,
                                email=email, website=website, website_nickname=website_nickname)
        return HttpResponseRedirect('/resources/edit')
