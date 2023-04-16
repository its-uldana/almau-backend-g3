from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(null=False, unique=True, blank=False, max_length=255)
    username = models.CharField(null=False, unique=True, blank=False, max_length=80)
    first_name = models.CharField(null=False, max_length=100, blank=False)
    last_name = models.CharField(null=False, max_length=100, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # email_verified = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class ResetPassword(models.Model):
    email = models.EmailField(null=False, blank=False, max_length=255)
    token = models.CharField(null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


