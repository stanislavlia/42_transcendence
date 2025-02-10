from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.forms import CustomUserCreationForm
from myapp.user_management.ft_api_usermanager import PongUserManager, FourtyTwoUserInfo
from myapp.models import CustomUserManager, CustomUser, Notification



@login_required
def notifications_view(request):
    notifications = request.user.notifications.order_by("-created_at")

    

    return render(request, "myapp/notifications.html", {"notifications": notifications})


@login_required
def read_all_notifications_view(request):
    
    request.user.read_all_notifications()

    return redirect("notifications_view")

@login_required
def delete_notification_view(request, notification_id):

    # Retrieve the notification that belongs to the current user.
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    
    # Delete the notification.
    notification.delete()
    
    
    return redirect("notifications_view")