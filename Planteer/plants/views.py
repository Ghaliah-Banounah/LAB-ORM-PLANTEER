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
        else:
            print(plantData.errors)
        response = redirect('main:homeView')

    return response

#Plant details view
def plantDetailsView(request: HttpRequest, plantid:int):

    #Check if the ID is valid or display a 404
    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = redirect('main:notFoundView')
    else:
        response = render(request, 'plants/plantDetails.html', context={"plant":plant})
    
    return response

#Update plant view
def updatePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = redirect('main:notFoundView')
    else:

        response = render(request, 'plant/updatePlant.html', context={"plant":plant, "categories":Plant.Categories.choices})
        if request.method == "POST":
            #Update existing plant
            plantData = PlantForm(request.POST, request.FILES, instance=plant)
            if plantData.is_valid():
                plantData.save()

            response = redirect('plant:plantDetailsView', plantid=plant.id)

    return response

#Delete plant view
def deletePlantView(request: HttpRequest, plantid:int):

    try:
        plant = Plant.objects.get(pk=plantid)
    except Exception:
        response = redirect('main:notFoundView')
    else:
        plant.delete()
        response = redirect('main:homeView')
    return response

#Filter by category or display all view
def plantsDisplayView(request: HttpRequest, filterBy):

    plants = Plant.objects.filter(category=filterBy).order_by('createdAt') if filterBy != "all" else Plant.objects.all().order_by('createdAt')
    if "isEdible" in request.GET:
        plants = plants.filter()
    
    response = render(request, 'plants/allPlants.html', context={'plants': plants, 'categories': Plant.Categories.choices, 'selected': filterBy})
    return response

def searchPlantsView(request:HttpRequest):

    if "search" in request.GET and len(request.GET["search"]) >= 3:
        plants = Plant.objects.filter(title__contains=request.GET["search"])
    else:
        plants = []

    return render(request, "plants/searchPlants.html", {"plants" : plants})