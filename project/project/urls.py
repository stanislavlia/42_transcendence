"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from myapp import views



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('', views.home),

    path('profile/', views.profile_view, name="profile"),
    path('games/', views.games_history_page, name="games"),
    path('users/', views.users_page, name="users"),


    

    path('login/', views.login_view, name="login"),
    path('authorize/', views.authorize_42_student, name='authorize_42'),
    path('auth/callback/42', views.handle_callback_from_42provider, name='handle_42_callback'),
]
