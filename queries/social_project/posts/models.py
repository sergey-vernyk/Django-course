from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Category(models.Model):
    """Модель категорії."""

    title = models.CharField(max_length=180, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=["title"])]

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    """Модель поста."""

    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
