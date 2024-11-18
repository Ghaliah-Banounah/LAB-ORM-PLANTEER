from django.db import models

class Plant(models.Model):
    class Categories(models.TextChoices):
        HERBS = "herbs", "Herbs"
        SHRUBS = "shrubs", "Shrubs"
        TREES = "trees", "Trees"
        CREEPERS = "creepers", "Creepers"
        CLIMBERS = "climbers", "Climbers"

    name = models.CharField(max_length=256)
    about  = models.TextField()
    usedFor = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=64, choices=Categories.choices)
    isEdible = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
