from django.contrib import admin
from .models import Purpose, Recipe

@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'cooking_time']
    search_fields = ['title', 'ingredients', 'instructions']
    filter_horizontal = ['purposes'] 