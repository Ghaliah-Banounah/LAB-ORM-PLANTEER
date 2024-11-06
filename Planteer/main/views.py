from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant

#Home page
def homeView(request: HttpRequest):
    
    plants = Plant.objects.all()[0:3]

    return render(request ,'main/home.html', context={'plants':plants})

#Mode change
def modeView(request: HttpRequest, mode):
    response = redirect(request.GET.get("next", "/"))
    
    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")
        
    return response

#Handling wrong entry
def notFoundView(request: HttpRequest):
    
    return render(request, '404.html')