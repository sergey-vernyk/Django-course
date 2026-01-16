from typing import Any

from rest_framework import serializers

from .models import Author, Book, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """Серіалайзер для створення та оновлення публікатора книги."""

    website = serializers.URLField()

    class Meta:
        model = Publisher
        fields = ("id", "name", "website")


class AuthorSerializer(serializers.ModelSerializer):
    """Серіалайзер для створення та оновлення автора книги."""

    email = serializers.EmailField()

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "email")


class BookSerializer(serializers.ModelSerializer):
    """Серіалайзер для створення та оновлення книги разом з її публікатором та авторами."""

    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    publication_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Book
        fields = ("id", "title", "authors", "publisher", "publication_date", "pages")
