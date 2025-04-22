"""
URL configuration for jackpot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views  # Import Django's built-in auth views
from jackpot import views  # Import views from the jackpot module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("manager", views.manager, name='manager'),  # Fixed missing view argument
    path("settings", views.settings, name='settings'),
    path("dashboard", views.dashboard.as_view(), name='dashboard'),  # Fixed typo in URL path
    # Using Django's built-in authentication views
    path("login", views.Login.as_view(), name='login'),
    path("logout", auth_views.LogoutView.as_view(), name='logout'),
     path('register', views.RegisterView.as_view(), name='register'),  # RegisterView as a class-based view,  # Make sure RegisterView is defined in your views
    path("password_reset", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("password_change", auth_views.PasswordChangeView.as_view(), name='password_change'),
    path("password_reset_done", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
