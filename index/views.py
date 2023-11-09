from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
def index_view(request):
    return render(request, 'index/index.html')


def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email
        send_mail(
            'Contact Form: {} {}'.format(first_name, last_name),
            message,
            email,  # From email
            [settings.DEFAULT_FROM_EMAIL],  # To email, should be your email address
            fail_silently=False,
        )

        return HttpResponse('Thanks for contacting us!')

    return render(request, 'index/contact.html')
