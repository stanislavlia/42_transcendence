from django.shortcuts import render, redirect, get_object_or_404
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


def  view_user_profile(request, id):
    user_profile = get_object_or_404(CustomUser, id=id)


    context = {
        "id": user_profile.id,
        "first_name": user_profile.first_name,
        "last_name": user_profile.last_name,
        "username": user_profile.nickname,   
        "email": user_profile.email,
        "avatar_image": user_profile.avatar or DEFAULT_AVATAR_IMG,
        "registration_date": user_profile.registration_date,
        "myprofile_flag": False,
    }

    return render(request, 'myapp/profile.html', context=context)





@login_required(login_url='/login/')
def profile_view(request):
    """View your own profile"""

    user_id = request.user.id
    user : CustomUser = request.user #instance from db

    logger.debug(f"USER  {user.email} VIEWS HIS PROFILE")

    context = {"id" : user.id ,
                "first_name" : user.first_name,
               "email" : user.email,
               "username" : user.nickname,
               "avatar_image" : user.avatar if user.avatar else DEFAULT_AVATAR_IMG,
               "registration_date" : user.registration_date,
               "myprofile_flag" : True}
    

    return render(request, 'myapp/profile.html', context=context)



@login_required(login_url='/login/')
def games_history_page(request):
    return render(request, "myapp/games.html")



def users_page(request):

    users = CustomUser.objects.all().filter(is_active=True)

    return render(request, "myapp/users.html", context={"users" : users,
                                                        })


