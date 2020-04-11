from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Manager for creating user
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save new user
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # to encrypt password
        user.save(using=self._db)  # to work with diff dbs

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creates custom User model that supports email instead username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # use email as username

