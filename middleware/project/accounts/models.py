from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """Роль користувача в системі."""

    TEACHER = "teacher"
    ADMIN = "admin"
    STUDENT = "student"


class User(AbstractUser):
    """Модель користувача з додатковими полями."""

    role = models.CharField(choices=UserRole.choices, max_length=7)
