from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Resource
from django.core.paginator import Paginator
import resources
from itertools import groupby
from django.test import TestCase, Client
from django.urls import reverse
from .models import Resource


def resources_view(request):
    # Order resources by 'category'
    resources_ordered = Resource.objects.all().order_by('category')

    # Group resources by 'category'
    grouped_resources = {k: list(v) for k, v in groupby(resources_ordered, key=lambda r: r.category)}

    page_num = request.GET.get('page', 1)
    paginator = Paginator(list(grouped_resources.items()), 30)
    c_page = paginator.page(int(page_num))

    return render(request, 'resources/resources.html', locals())
