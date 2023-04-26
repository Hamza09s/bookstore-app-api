"""
Database models.
"""
# import uuid
# import os

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        # spelling is important otherwise django cli won't pick it
        # check these lines when issue with django admin login
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Book(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True
    )
    books = models.ManyToManyField(Book, blank=True)
    book_id = models.IntegerField(default=1)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
