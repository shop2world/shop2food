from django.db import models

class Purpose(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField(help_text="조리 시간(분)")
    purposes = models.ManyToManyField(Purpose, related_name='recipes')
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title