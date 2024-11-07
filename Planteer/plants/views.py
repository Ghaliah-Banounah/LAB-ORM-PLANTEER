from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant
from .forms import PlantForm

#New plant view 
def newPlantView(request:HttpRequest):
    
    #Using django forms to validate and save plant data 
    plantData = PlantForm()

    response = render(request, 'plants/createPlant.html', context={'categories':Plant.Categories.choices})
    
    if request.method == "POST":
        plantData = PlantForm(request.POST, request.FILES)
        if plantData.is_valid():
            plantData.save()
            
        response = redirect('main:plantsDisplayView' 'all')

    return response

#Plant details view
def plantDetailsView(request: HttpRequest, plantid:int):

    #Check if the ID is valid or display a 404
    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:
        similarPlants = Plant.objects.filter(category=plant.category)
        response = render(request, 'plants/plantDetails.html', context={"plant":plant, "similarPlants": similarPlants})
    
    return response

#Update plant view
def updatePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:

        response = render(request, 'plants/updatePlant.html', context={"plant":plant, "categories":Plant.Categories.choices})
        if request.method == "POST":
            #Update existing plant
            plantData = PlantForm(request.POST, request.FILES, instance=plant)
            if plantData.is_valid():
                plantData.save()
            print(plantData.errors)
            response = redirect('plants:plantDetailsView', plantid=plant.id)

    return response

#Delete plant view
def deletePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = render(request, '404.html')
    else:
        plant.delete()
        response = redirect('main:homeView')
    return response

#Filter by category or display all view
def plantsDisplayView(request: HttpRequest, filterBy):

    plants = Plant.objects.filter(category=filterBy).order_by('createdAt') if filterBy != "all" else Plant.objects.all().order_by('createdAt')
    if "isEdible" in request.GET and request.GET["isEdible"] == "true":
        plants = plants.filter(isEdible=True)
    elif "isEdible" in request.GET and request.GET["isEdible"] == "false":
        plants = plants.filter(isEdible=False)

    response = render(request, 'plants/allPlants.html', context={'plants': plants, 'categories': Plant.Categories.choices, 'selected': filterBy})
    return response

def searchPlantsView(request:HttpRequest):

    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(name__contains=request.GET["search"])
        if "category" in request.GET:
            plants = plants.filter(category=request.GET['category'])
        if "isEdible" in request.GET and request.GET["isEdible"] == "true":
            plants = plants.filter(isEdible=True)
        elif "isEdible" in request.GET and request.GET["isEdible"] == "false":
            plants = plants.filter(isEdible=False)
    else:
        plants = []

    return render(request, "plants/searchPlants.html", {"plants" : plants, 'categories': Plant.Categories.choices})
