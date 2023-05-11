"""
    URL configuration for authentication and profile functions
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('auth/register/', views.register_view, name="register"),
    path('auth/login/', views.login_view, name="login"),
    path('auth/logout/', views.logout_view, name="logout"),
    path('account/', views.account_view, name="account"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
