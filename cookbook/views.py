"""
    View functions for the core cookbook application
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request, "cookbook/index.html")