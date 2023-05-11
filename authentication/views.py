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

from .forms import RegistrationForm, LoginForm, UpdateProfileForm, UpdateAccountForm
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri

from .models import Profile
import os


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


# Change Account settings
@login_required
def account_view(request):
    # - POST request
    if request.method == "POST":
        # Profile picture form
            if request.POST.get("reset_pfp", None) == "reset":
                # Reset profile picture
                request.user.profile.picture = os.path.join("profile", "default.svg")
                request.user.profile.save()
            elif request.FILES.get("picture", None):
                # Update profile picture
                profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
                
                if profile_form.is_valid():
                    profile_form.save()
                else:
                    for errors in profile_form.errors["picture"].as_data():
                        for error in errors:
                            messages.error(request, error)
        
    # - GET request
    account_form = UpdateAccountForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    
    context = {
        "profile_form": profile_form,
        "account_form": account_form,
        "joined": request.user.date_joined,
    }
    
    return render(request, "authentication/account.html", context)