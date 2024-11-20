from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant
from .models import Contact
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib import messages

#Home page
def homeView(request: HttpRequest):
    
    plants = Plant.objects.all().order_by('-createdAt')[0:3]

    return render(request ,'main/home.html', context={'plants':plants})

#Contact us page
def contactView(request: HttpRequest):
    contactData = ContactForm()

    response = render(request, 'main/contactUs.html')
    
    if request.method == "POST":

        contactData = ContactForm(request.POST)
        if contactData.is_valid():
            contactData.save()

            subject = "Planteer Support"
            fromEmail = settings.DEFAULT_FROM_EMAIL
            to = request.POST['email']
            htmlContent = render_to_string('main/mail/mailTemplate.html', {'reciever': request.POST, 'sentAt': datetime.strftime(datetime.now() , "%d/%m/%Y, %H:%M:%S")})
            emailMsg = EmailMessage(subject, htmlContent,  fromEmail, [to])
            emailMsg.content_subtype = "html"
            emailMsg.send()
            messages.success(request, "Your message was sent successfully. Thank you.", "alert-success") 

    return response

#All messages page
def allMessagesView(request: HttpRequest):
    messages = Contact.objects.all().order_by("-createdAt")
    response = render(request, 'main/allMessages.html', context={'messages': messages})

    return response

#Mode change
def modeView(request: HttpRequest, mode):
    response = redirect(request.GET.get("next", "/"))
    
    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")
        
    return response
