"""
    Form classes for cookbook realted pages
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""

from django.urls import reverse
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Recipe


# General recipe information
class RecipeGeneralForm(forms.ModelForm):

    picture = forms.ImageField(widget=forms.FileInput, required=False)
    title = forms.CharField(label="Recipe title", max_length=255, required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, max_length=1000, required=False)
    servings = forms.FloatField(
        label="Servings", initial=1, min_value=0,required=True,
        widget=forms.NumberInput(attrs={'step': "0.01"})
    )

    
    class Meta:
        model = Recipe
        fields = ["picture", "title", "description", "servings"]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "form-label"

        self.fields['picture'].label = False

        self.helper.layout = Layout(
            Div(
                HTML("""
                    <label for="recipe-picture">
                        <img class="image-preview" src="" alt="">
                    </label>
                """),
                Field("picture", css_class="image-input", id="recipe-picture"),
                HTML("""<a class="btn btn-danger remove-image-file-btn" id="remove-profile-picture-btn">Remove Picture</a>"""),
                css_class="image-upload-cont mb-3"
            ),
            FloatingField("title"),
            FloatingField("description"),
            FloatingField("servings")
        )


# Recipe ingredient with quantity and measurement
class RecipeIngredientForm(forms.Form):

    ingredient_name = forms.CharField(
        max_length=255, label="Ingredient",
        widget=forms.TextInput(attrs={'placeholder': 'Ingredient'}
    ))

    quantity = forms.CharField(
        max_length=20, label="Quantity",
        widget=forms.TextInput(attrs={'placeholder': 'Quantity'}
    ))
    
    measurement = forms.CharField(
        max_length=20, label="Measurement",
        widget=forms.TextInput(attrs={'placeholder': 'Measurement'}
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "form-label"

        self.helper.layout = Layout(
            Div(
                FloatingField("ingredient_name"),
                Row(
                    Column(
                        FloatingField("quantity"),
                        css_class="col-6"
                    ),
                    Column(
                        FloatingField("measurement"),
                        css_class="col-6"
                    )
                ),
                css_class="container"
            )
        )


# Recipe instruction
class RecipeInstructionForm(forms.Form):

    instruction = forms.CharField(
        max_length=255, label=False,
        widget=forms.TextInput(attrs={'placeholder': 'Instruction'}
    ))


class RecipeInstructionFormHelper(FormHelper):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.label_class = "form-label"

        self.layout = Layout(
            Row(
                Column(
                    HTML("<span class='instruction-number'>1.</span>"),
                    css_class="col-1"
                ),
                Column(
                    Field("instruction"),
                    css_class="col-10"
                ),
                Column(
                    HTML("<a class='btn btn-danger'>-</a>"),
                    css_class="col-1"
                ),
                css_class="instruction-input-group"
            )
        )