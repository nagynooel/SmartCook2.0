"""
    View functions for the core cookbook application
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Dashboard
@login_required
def index_view(request):
    return render(request, "cookbook/index.html")