from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# User repository functions
class CustomUserManager(BaseUserManager):
    # Create a new user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Create a new admin user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

# User model
class CustomUser(AbstractUser):
    # Role choices enum (trailing ',' for python tuple notation)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('viewer', 'View-Only'),
    ]
    # Remove username, using emails for auth
    username = None

    # Define required fields
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # Define custom access roles
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    # Attach custom manager to get additional fields
    objects = CustomUserManager()

    # Use email for login
    USERNAME_FIELD = 'email'
    # Additional required fields (above Django defaults: email, password etc)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # ToString() Equivalent
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    # IsAdmin Getter 
    @property
    def is_admin(self):
        return self.role == 'admin'