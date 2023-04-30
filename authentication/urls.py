"""
    URL configuration for authentication and profile functions
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_view, name="register"),
    path('auth/login/', views.login_view, name="login"),
    path('auth/logout/', views.logout_view, name="logout"),
]
