from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    email_sent = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email


class Application(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(max_length=30, default="pending")
    external_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email}:{self.status}:{self.external_id}"
