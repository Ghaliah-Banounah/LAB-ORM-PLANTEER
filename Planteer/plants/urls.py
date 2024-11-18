from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("new/", views.newPlantView, name="newPlantView"),
    path("plantdetails/<int:plantid>/", views.plantDetailsView, name="plantDetailsView"),
    path("update/<int:plantid>/", views.updatePlantView, name="updatePlantView"),
    path("delete/<int:plantid>/", views.deletePlantView, name="deletePlantView"),
    path("category/<filterBy>/", views.plantsDisplayView, name="plantsDisplayView"),
    path("search/", views.searchPlantsView, name="searchPlantsView"),
    path("comments/add/<int:plantid>", views.addCommentView, name="addCommentView"),
]