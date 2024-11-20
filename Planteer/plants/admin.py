from django.contrib import admin
from .models import Plant, Comment, Category

class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'createdAt']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'createdAt']
    list_filter = ['plant']

admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
