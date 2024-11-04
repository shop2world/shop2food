from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_recipes(request):
    return redirect('recipes:home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('', redirect_to_recipes, name='home'),
] 