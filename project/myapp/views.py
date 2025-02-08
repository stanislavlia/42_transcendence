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
    return render(request, 'myapp/profile.html')



@login_required(login_url='/login/')
def games_history_page(request):
    return render(request, "myapp/games.html")



@login_required(login_url='/login/')
def users_page(request):
    return render(request, "myapp/users.html")



#=============USER MANAGEMENT ===================
#TODO: move to separate file .py


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            logger.info(f'NEW USER REGISTERED | user: {user.email}')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #goes to Db, search for user, compare password hash and return instance
        user = authenticate(request, username=email, password=password)


        if user is not None:
            logger.info(f"USER LOGGED IN: {user.email}")

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'myapp/login.html')



def authorize_42_student(request):

    user_manager = PongUserManager()
    authorization_url, state = user_manager.get_authorization_url()

    logger.info(f"oauth_state: {state} | auth_url: {authorization_url}")

    request.session["oauth_state"] = state
    return redirect(authorization_url)


def handle_callback_from_42provider(request):

    code = request.GET.get('code')

    manager = PongUserManager()
    manager.fetch_token(code=code)

    user_info : FourtyTwoUserInfo = manager.extract_fields_from_user_info(manager.get_user_info())
    
    logger.debug(f"USER AUTHENTICATED FROM 42 PROVIDER | user : {user_info}")

    return redirect('home')