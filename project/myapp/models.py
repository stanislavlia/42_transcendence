from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from loguru import logger
from enum import Enum
from django.urls import reverse


# ==================== MANAGERS ====================
class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling the creation and management of CustomUser instances.

    Provides methods to create regular users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the specified email and password.

        Args:
            email (str): The user's email address, serving as the unique identifier.
            password (str, optional): The user's password. Defaults to None.
            **extra_fields: Additional fields to include in the user profile.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        logger.info(f"created user with email {email}")
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the specified email and password.

        Args:
            email (str): The superuser's email address.
            password (str): The superuser's password.
            **extra_fields: Additional fields to include in the superuser profile.

        Raises:
            ValueError: If 'is_staff' or 'is_superuser' are not set to True.

        Returns:
            CustomUser: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        logger.info(f"created super-user with email {email}")
        return self.create_user(email, password, **extra_fields)



# ==================== MODELS ====================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for authentication.

    Replaces Django's default User model, using email as the unique identifier
    instead of a username. Includes additional fields such as nickname,
    registration_date, avatar, oauth_provider, and oauth_id.
    """

    email = models.EmailField(unique=True, null=False)
    nickname = models.CharField(max_length=100, blank=True, null=False)
    first_name = models.CharField(max_length=150, blank=True, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    
    registration_date = models.DateTimeField(auto_now_add=True)

    avatar = models.URLField(blank=True, null=True)
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    oauth_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        """
        Return a string representation of the user.

        Returns:
            str: The user's email address.
        """
        return self.email
    
    def get_profile_link(self):
        """
        Returns the URL to the user's profile page.
        Assumes you have a URL pattern named 'view_user_profile' that takes the user ID as an argument.
        """
        return reverse('view_user_profile', args=[self.id])





class   FriendShipStatuses(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REVOKED = "revoked"
    REJECTED = "rejected"

    @classmethod
    def get_list_of_choices(cls):
        # Returns a list of tuples: (value, human-readable label)
        return [(status.value, status.value.capitalize()) for status in cls]
    
 
class Friendship(models.Model):
    """Models Friendship between two users. Friendship can be in status: pending, accepted, revoked, rejected"""

    from_user = models.ForeignKey(
        'myapp.CustomUser',
        related_name='friendship_requests_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        'myapp.CustomUser',
        related_name='friendship_requests_received',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=FriendShipStatuses.get_list_of_choices(),
        default=FriendShipStatuses.PENDING.value,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Friendship: {self.from_user} -> {self.to_user} [{self.status}]"