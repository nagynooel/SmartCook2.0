from django.db import models
from cookbook.storage import OverwriteStorage


def rename_file(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance.id}.{ext}"
    return f"recipe/{filename}"


# Recipe related models
class Ingredient(models.Model):
    verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    trans_fat = models.FloatField()
    cholesterol = models.FloatField()
    sodium = models.FloatField()
    carbohydrates = models.FloatField()
    fiber = models.FloatField()
    sugar = models.FloatField()
    protein = models.FloatField()


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=20)


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    picture = models.ImageField(default="recipe/default.svg", upload_to=rename_file, storage=OverwriteStorage())
    servings = models.FloatField()


class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20)


class RecipeInstruction(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction = models.CharField(max_length=1000)