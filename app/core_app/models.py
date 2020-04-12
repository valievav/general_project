from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Manager for creating user
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates new user
        """
        if not email:
            raise ValueError('Please provide an email, this field is obligatory')

        email = self.normalize_email(email)  # lowercase domain part (username part can be case sensitive)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # to encrypt password as hash
        user.save(using=self._db)  # to work with diff db types

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates superuser
        """
        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


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
