"""
    View functions for the core cookbook application
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory
from .forms import (
    RecipeGeneralForm,
    RecipeIngredientForm,
    RecipeInstructionForm,
    RecipeInstructionFormHelper
)

# Dashboard
@login_required
def index_view(request):
    return render(request, "cookbook/index.html")


@login_required
def create_new_recipe_view(request):
    context = {
        "generalForm":RecipeGeneralForm(),
        "ingredientForm":RecipeIngredientForm(),
        "instructionForm":formset_factory(RecipeInstructionForm, extra=4),
        "instructionFormHelper":RecipeInstructionFormHelper(),
    }

    return render(request, "cookbook/new_recipe.html", context)