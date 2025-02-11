
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from loguru import logger
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.forms import CustomUserCreationForm
from myapp.user_management.ft_api_usermanager import PongUserManager, FourtyTwoUserInfo
from myapp.models import CustomUserManager, CustomUser


##==================ENDPOINTS TO MANAGE USER REGISTRATION/LOGIN/AUTH=============================
def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

        

            user.set_password(form.cleaned_data['password1'])
            user.save()
            logger.info(f'REGISTRATION | NEW USER REGISTERED | user: {user.email}')
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
        user : CustomUser = authenticate(request, username=email, password=password)


        if user is not None:
            logger.info(f"USER LOGGED IN: {user.email}")

            login(request, user)

            return redirect("home") #successful login
            
        else:
            logger.warning(f"USER FAILED TO LOGIN... | he tried email: {email}")
            failed_context = {"is_failed" : True,
                              "fail_reason" : "User does not exist"}
            return render(request, 'myapp/login.html', context=failed_context)
        

    return render(request, 'myapp/login.html')



def logout_view(request):
    logger.info(f"LOGOUT USER: {request.user.email}")
    logout(request)

    return redirect("home")



def authorize_42_student(request):
    """Endpoint to authorize 42 student using Oauth"""

    user_manager = PongUserManager()
    authorization_url, state = user_manager.get_authorization_url()

    logger.info(f"oauth_state: {state} | auth_url: {authorization_url}")

    request.session["oauth_state"] = state
    return redirect(authorization_url)




def handle_callback_from_42provider(request):
    """Endpoint to receive callback with data about 42 student"""
    
    code = request.GET.get('code')

    manager = PongUserManager()
    manager.fetch_token(code=code)

    user_info: FourtyTwoUserInfo = manager.extract_fields_from_user_info(manager.get_user_info())
    
    try:
        user = CustomUser.objects.get(email=user_info.email)
        logger.info(f"EXISTING USER AUTHENTICATED FROM 42 PROVIDER | user: {user.email}")
    except CustomUser.DoesNotExist:
        logger.info(f"NEW USER REGISTERED VIA 42 INTRA OAUTH | user: {user_info.email}")
        user = CustomUser.objects.create_user(
            email=user_info.email,
            nickname=user_info.login,
            oauth_provider="42",
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            avatar=user_info.avatar_image_link,
            password=None  # No password since login is via 42 Intra
        )
    
    # Log the user in by attaching them to the session
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    
    return redirect('home')




#======================ENDPOINTS TO MODIFY USER PROPERTIES==================

@login_required
def modify_description(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Only allow the user to modify their own description
    if request.user != user:
        logger.error(f"Cannot modify desciption of another user...")
        return redirect('profile')

    if request.method == 'POST':
        # Get the new description from the form submission
        new_description = request.POST.get('description', '').strip()
        user.description = new_description
        user.save()
        logger.info(f"User: {user.email} updated his description")
        return redirect('profile')
    else:
        context = {
            'user': user,  # includes user.description
        }
        return render(request, 'myapp/modify_description.html', context)
