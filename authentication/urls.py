"""
    URL configuration for authentication and profile functions
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('auth/register/', views.register_view, name="register"),
    path('auth/login/', views.login_view, name="login"),
    path('auth/logout/', views.logout_view, name="logout"),
    path('account/', views.account_view, name="account"),
    path('account/reset-password/email', views.send_password_reset_email_view, name="send_password_reset_email"),
    path('account/reset-password/<str:token>', views.reset_password_view, name="reset_password"),
    path('account/forgotten-password', views.send_forgotten_password_email_view, name="forgotten_password")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
