from django.db import models
from companies.models import Company
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class DeveloperManager(BaseUserManager):
    """
    Custom manager for Developer model.
    """
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)  # Allow access to admin
        extra_fields.setdefault('is_superuser', True)  # Superuser permissions
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, first_name, last_name, password, **extra_fields)


class Developer(AbstractBaseUser, PermissionsMixin):
    """
    Custom Developer model inheriting from AbstractBaseUser.
    """
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (9 to 15 digits)."
            )
        ]
    )
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    # Permissions fields
    is_staff = models.BooleanField(default=False)  # For admin access
    is_superuser = models.BooleanField(default=False)  # For full permissions
    is_active = models.BooleanField(default=True)  # For account activation

    # Add the required fields for user creation
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    # Custom Manager
    objects = DeveloperManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the full name of the developer."""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Return the short name of the developer (first name)."""
        return self.first_name

    class Meta:
        ordering = ['last_name', 'first_name']
