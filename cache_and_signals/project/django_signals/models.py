from django.contrib.auth import get_user_model
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(
        get_user_model(),
        related_name="project",
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.name)
