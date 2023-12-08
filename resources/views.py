from itertools import groupby

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.test import Client, TestCase
from django.urls import reverse

import resources

from .models import Resource


# handles the display of resources on the Resources page
def resources_view(request):
    # Order resources by 'category'
    resources_ordered = Resource.objects.all().order_by('category')

    # Group resources by 'category'
    grouped_resources = {k: list(v) for k, v in groupby(resources_ordered, key=lambda r: r.category)}

    page_num = request.GET.get('page', 1)
    paginator = Paginator(list(grouped_resources.items()), 30)
    c_page = paginator.page(int(page_num))

    return render(request, 'resources/resources.html', locals())
