from django import forms

from .models import Category, Post


class CategoryForm(forms.ModelForm):
    """Форма для створення або оновлення категорії."""

    class Meta:
        model = Category
        fields = ("title", "description")


class PostForm(forms.ModelForm):
    """Форма для створення або оновлення поста."""

    class Meta:
        model = Post
        fields = ("title", "content", "categories")
