from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionManager


class UserManager(BaseUserManager):
    """Custom user manager class"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must has email address')

        username = ''
        if extra_fields.get('username'):
            username = extra_fields.get('username')
            extra_fields.pop('username')
        else:
            username = email.split('@')[0]

        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new super user"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionManager):
    """Custom user model that supports using email instead of username"""

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have a specific permission"""
        return self.is_superuser

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
