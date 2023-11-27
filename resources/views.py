from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Resource
from django.core.paginator import Paginator
import resources
from itertools import groupby
from django.test import TestCase, Client
from django.urls import reverse
from .models import Resource


class ResourceViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test data if necessary

    def test_resources_view(self):
        response = self.client.get(reverse('resources_view'))
        self.assertEqual(response.status_code, 200)
        # Add assertions to check the context data and template

    def test_edit_resources_get(self):
        response = self.client.get(reverse('edit_resources'))
        self.assertEqual(response.status_code, 200)
        # Verify the correct template is used

    def test_delete_post(self):
        resource = Resource.objects.create(name='Test Resource')
        response = self.client.post(reverse('delete', args=[resource.id]))
        self.assertFalse(Resource.objects.filter(id=resource.id).exists())
        self.assertRedirects(response, '/resources/edit')

    def test_modify_get_post(self):
        resource = Resource.objects.create(name='Old Name')
        response = self.client.get(reverse('modify', args=[resource.id]))
        self.assertEqual(response.status_code, 200)
        # Test POST request
        response = self.client.post(reverse('modify', args=[resource.id]), {
            'name': 'New Name',
            # include other fields
        })
        resource.refresh_from_db()
        self.assertEqual(resource.name, 'New Name')
        self.assertRedirects(response, '/resources/edit')

    def test_add_get_post(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        # Test POST request
        response = self.client.post(reverse('add'), {
            'name': 'New Resource',
            # include other fields
        })
        self.assertTrue(Resource.objects.filter(name='New Resource').exists())
        self.assertRedirects(response, '/resources/edit')


# Make sure to replace `reverse('view_name')` with the actual names of your URL patterns


def resources_view(request):
    # Order resources by 'category'
    resources_ordered = Resource.objects.all().order_by('category')

    # Group resources by 'category'
    grouped_resources = {k: list(v) for k, v in groupby(resources_ordered, key=lambda r: r.category)}

    page_num = request.GET.get('page', 1)
    paginator = Paginator(list(grouped_resources.items()), 3)
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
