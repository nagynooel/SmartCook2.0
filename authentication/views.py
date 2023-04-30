"""
    View functions for authentication and profile related pages
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri


# Register new user page
def register_view(request):
    context = None
    
    if request.method == "POST":
        # Populate form with data
        form = RegistrationForm(request.POST)
        
        # Validate form
        if form.is_valid():
            # Create user and log them in
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))
        
        context = {"form":form}
        
    
    # Only create empty form if POST request result form does not exists
    context = context or {"form":RegistrationForm()}
    
    return render(request, "authentication/register.html", context)


# Login page
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check for a next url and redirect user there if valid
            next = request.POST.get("next", "")
            
            if next != "" and url_has_allowed_host_and_scheme(next, None):
                return redirect(iri_to_uri(next))
            
            return redirect(reverse("index"))
        
        messages.error(request, "Username or password is not correct!")
    
    context = {"form":LoginForm(), "next":request.GET.get("next", "/")}
    
    return render(request, "authentication/login.html", context)


# Logout user
@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))