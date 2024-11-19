from django.contrib import admin
from .models import Plant, Comment

class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'createdAt']
    list_filter = ['category']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'createdAt']
    list_filter = ['plant']

admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
