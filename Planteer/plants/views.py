from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant, Comment, Category
from .forms import PlantForm
from django.core.paginator import Paginator
from django.contrib import messages

#New plant view 
def newPlantView(request:HttpRequest):
    
    #Using django forms to validate and save plant data 
    plantData = PlantForm()

    categories = Category.objects.all()
    response = render(request, 'plants/createPlant.html', context={'categories':categories})
    
    if request.method == "POST":
        plantData = PlantForm(request.POST, request.FILES)
        if plantData.is_valid():
            plantData.save()
            messages.success(request, f"'{request.POST['name']}' added successfully.", "alert-success")    
            
        response = redirect('plants:plantsDisplayView', 'all')

    return response

#Plant details view
def plantDetailsView(request: HttpRequest, plantid:int):

    #Check if the ID is valid or display a 404
    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:
        comments = Comment.objects.filter(plant=plant)
        similarPlants = Plant.objects.exclude(pk=plantid).filter(categories__in=plant.categories.all())[0:3]
        response = render(request, 'plants/plantDetails.html', context={"plant":plant, "similarPlants": similarPlants, "comments": comments})
    
    return response

#Update plant view
def updatePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:

        categories = Category.objects.all()
        response = render(request, 'plants/updatePlant.html', context={"plant":plant, "categories":categories})
        if request.method == "POST":
            #Update existing plant
            plantData = PlantForm(request.POST, request.FILES, instance=plant)
            if plantData.is_valid():
                plantData.save()
                messages.success(request, f"'{plant.name}' updated successfully.", "alert-success")    

            response = redirect('plants:plantDetailsView', plantid=plant.id)

    return response

#Delete plant view
def deletePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:
        try:
            plant.delete()
        except Exception:
            messages.error(request, f"'{plant.name}' wasn't deleted.", "alert-danger")
        else: 
            messages.success(request, f"'{plant.name}' deleted successfully.", "alert-success")    
        
        response = redirect('main:homeView')
    return response

#Filter by category or display all view
def plantsDisplayView(request: HttpRequest, filterBy:str):

    if filterBy == 'all':
        plants = Plant.objects.all().order_by('-createdAt')
    else:
        plants = Plant.objects.filter(categories__name__in=[filterBy]).order_by('-createdAt')##

    if "isEdible" in request.GET and request.GET["isEdible"] == "true":
        plants = plants.filter(isEdible=True)
    elif "isEdible" in request.GET and request.GET["isEdible"] == "false":
        plants = plants.filter(isEdible=False)

    categories = Category.objects.all()
    paginator = Paginator(plants, 6)
    pageNumber = request.GET.get('page', 1)
    page_obj = paginator.get_page(pageNumber)

    response = render(request, 'plants/allPlants.html', context={'categories': categories, 'selected': filterBy, 'page_obj': page_obj })
    return response

def searchPlantsView(request:HttpRequest):

    if "search" in request.GET and len(request.GET["search"]) >= 3:

        plants = Plant.objects.filter(name__contains=request.GET["search"]).order_by('-createdAt')
        if "categories" in request.GET:
            plants = plants.filter(categories__name__in=request.GET['categories'])##
        if "isEdible" in request.GET and request.GET["isEdible"] == "true":
            plants = plants.filter(isEdible=True)
        elif "isEdible" in request.GET and request.GET["isEdible"] == "false":
            plants = plants.filter(isEdible=False)
    else:
        plants = []

    categories = Category.objects.all()
    paginator = Paginator(plants, 6)
    pageNumber = request.GET.get('page', 1)
    page_obj = paginator.get_page(pageNumber)

    response = render(request, 'plants/searchPlants.html', {"page_obj":page_obj, 'categories':categories})
    return response

#Add comment to plants view
def addCommentView(request:HttpRequest, plantid:int):
    
    if request.method == 'POST':
        plant = Plant.objects.get(pk=plantid)
        newComment = Comment(plant=plant, name=request.POST['name'], comment=request.POST['comment'])
        newComment.save()

    return redirect('plants:plantDetailsView', plantid=plantid)