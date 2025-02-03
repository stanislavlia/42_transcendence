from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from loguru import logger



# Create your views here.
def home(request):
    logger.info(f"home page / queried | request: {request}")

    return HttpResponse("Welcome to the Home Page!")




#=============AUTH-related views===================
#TODO: move to separate file .py

from myapp.user_management.ft_api_usermanager import PongUserManager


def authorize_42_student(request):

    user_manager = PongUserManager()
    authorization_url, state = user_manager.get_authorization_url()

    logger.info(f"oauth_state: {state} | auth_url: {authorization_url}")

    request.session["oauth_state"] = state
    return redirect(authorization_url)


def handle_callback_from_42provider(request):

    code = request.GET.get('code')

    manager = PongUserManager()
    token = manager.fetch_token(code=code)

    user_info = manager.get_user_info(token)

    logger.debug(f"GET INFO: {user_info}")

    return redirect('home')