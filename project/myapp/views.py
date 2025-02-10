from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from myapp.user_management.ft_api_usermanager import PongUserManager, FourtyTwoUserInfo
from .models import CustomUserManager, CustomUser


DEFAULT_AVATAR_IMG = "https://cdn-icons-png.freepik.com/512/164/164440.png"


def home(request):

    return render(request, 'myapp/home.html')



#==========================INFO PAGES========================

@login_required(login_url='/login/')
def profile_view(request):


    user_id = request.user.id
    user : CustomUser = request.user #instance from db

    logger.debug(f"USER  {user.email} VIEWS HIS PROFILE")

    context = {"first_name" : user.first_name,
               "email" : user.email,
               "username" : user.nickname,
               "avatar_image" : user.avatar if user.avatar else DEFAULT_AVATAR_IMG,
               "registration_date" : user.registration_date}

    return render(request, 'myapp/profile.html', context=context)



@login_required(login_url='/login/')
def games_history_page(request):
    return render(request, "myapp/games.html")



def users_page(request):

    users = CustomUser.objects.all().filter(is_active=True)

    return render(request, "myapp/users.html", context={"users" :users})


