from django.shortcuts import render
from django.http import JsonResponse
import random
from .models import Purpose, Recipe

def home(request):
    purposes = Purpose.objects.all()
    return render(request, 'recipes/home.html', {'purposes': purposes})

def get_recipe(request):
    purpose_id = request.GET.get('purpose_id')
    try:
        purpose = Purpose.objects.get(id=purpose_id)
        recipes = list(purpose.recipes.all())
        if recipes:
            recipe = random.choice(recipes)
            return JsonResponse({
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'cooking_time': recipe.cooking_time,
                'image_url': recipe.image_url
            })
        return JsonResponse({'error': '해당 목적의 레시피가 없습니다.'}, status=404)
    except Purpose.DoesNotExist:
        return JsonResponse({'error': '잘못된 목적입니다.'}, status=404) 