from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self) -> str:
        return self.name


class Plant(models.Model):
    # class Categories(models.TextChoices):
    #     HERBS = "herbs", "Herbs"
    #     SHRUBS = "shrubs", "Shrubs"
    #     TREES = "trees", "Trees"
    #     CREEPERS = "creepers", "Creepers"
    #     CLIMBERS = "climbers", "Climbers"

    name = models.CharField(max_length=256)
    about  = models.TextField()
    usedFor = models.TextField()
    image = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField(Category)
    isEdible = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class Comment(models.Model):

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} on {self.plant.name}"
