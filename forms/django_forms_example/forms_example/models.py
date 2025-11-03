from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    email = models.EmailField(
        verbose_name="Email address",
        max_length=60,
        unique=True,
    )
    gender = models.CharField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        verbose_name="Gender",
    )
    photo = models.ImageField(blank=True, verbose_name="Profile photo")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date of birth")
    country = models.CharField(
        choices=[
            ("Ukraine", "Ukraine"),
            ("Germany", "Germany"),
            ("Slovakia", "Slovakia"),
            ("Poland", "Poland"),
            ("USA", "USA"),
            ("Italy", "Italy"),
        ],
        verbose_name="Country",
    )
    description = models.TextField(blank=True, verbose_name="Description")

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email
