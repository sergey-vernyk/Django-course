from django.db import models


class Category(models.Model):
    title = models.CharField(verbose_name="Назва", max_length=100)
    created_at = models.DateTimeField(verbose_name="Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)


class Article(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=200)
    slug = models.SlugField(verbose_name="Slug", unique=True)
    content = models.TextField(verbose_name="Текст")
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        on_delete=models.CASCADE,
        related_name="articles",
    )
    is_published = models.BooleanField(
        verbose_name="Опубліковано", default=False, help_text="Статус публікації статті"
    )
    created_at = models.DateTimeField(verbose_name="Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["title"]

    def __str__(self):
        return str(self.title)
