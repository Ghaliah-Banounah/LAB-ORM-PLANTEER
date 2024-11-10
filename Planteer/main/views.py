from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant
from .models import Contact
from .forms import ContactForm
from django.core.mail import send_mail
from Planteer import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

#Home page
def homeView(request: HttpRequest):
    
    plants = Plant.objects.all()[0:3]

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
            htmlContent = render_to_string('main/mailTemplate.html', {'reciever': request.POST, 'sentAt': datetime.strftime( datetime.now() , "%d/%m/%Y, %H:%M:%S")})
            textContent = strip_tags(htmlContent)
            send_mail(subject, textContent, fromEmail, [to], html_message=htmlContent, fail_silently=False)
            

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
