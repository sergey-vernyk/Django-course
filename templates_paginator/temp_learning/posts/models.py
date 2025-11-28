from django.db import models
from django.utils import timezone


class Author(models.Model):
    """Автор постів."""

    name = models.CharField(max_length=100)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    """Категорія поста."""

    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    """Пост з прив'язаними категорією та автором."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.title)
