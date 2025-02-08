from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from myapp.user_management.ft_api_usermanager import PongUserManager, FourtyTwoUserInfo
from .models import CustomUserManager, CustomUser


@login_required(login_url='/login/')
def home(request):

    return render(request, 'myapp/home.html')



#==========================INFO PAGES========================

@login_required(login_url='/login/')
def profile_view(request):
    # will be added later

    user_id = request.user.id
    user : CustomUser = request.user

    logger.debug(f"USER  {user.email} VIEWS HIS PROFILE")

    context = {"first_name" : user.first_name,
               "email" : user.email,
               "username" : user.nickname}

    return render(request, 'myapp/profile.html', context=context)



@login_required(login_url='/login/')
def games_history_page(request):
    return render(request, "myapp/games.html")



@login_required(login_url='/login/')
def users_page(request):
    return render(request, "myapp/users.html")


