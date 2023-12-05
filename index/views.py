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

        # Construct the message
        full_message = f"From: {first_name} {last_name}, Email: {email}\n\n{message}"

        # Send an email
        send_mail(
            f'Contact Form: {first_name} {last_name}',
            full_message,
            settings.EMAIL_HOST_USER,  # From email, use your email configured in settings
            [settings.EMAIL_HOST_USER],  # To email, should be your email address
        )

        return HttpResponse('Thanks for contacting us!')

    return render(request, 'index/contact.html')
