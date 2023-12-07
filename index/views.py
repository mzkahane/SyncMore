from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# handles requests to view the Home Page
def index_view(request):
    return render(request, 'index/index.html')


# handles requests to view the Contact Us page and form submissions when users submit a form to email SyncMore.
# It constructs a message from the information the user provides and sends an email to what is specified by the EMAIL_HOST_USER
def contact_view(request):
    if request.method == 'POST':
        # get information from the form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the message
        full_message = f"From: {first_name} {last_name}, Email: {email}\n\n{message}"

        # Send an email
        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,  # From email, use your email configured in settings
            [settings.EMAIL_HOST_USER],  # To email, should be your email address
        )

        # Add a success message
        messages.success(request, 'Your email has been sent successfully!')

        return HttpResponseRedirect('/index/contact/')

    return render(request, 'index/contact.html')
