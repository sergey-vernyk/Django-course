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

    def create(self, validated_data: dict[str, Any]) -> Book:
        authors_data = validated_data.pop("authors", None)
        publisher_data = validated_data.pop("publisher", None)

        print(authors_data)
        print(publisher_data)
        print(validated_data)

        publisher, _ = Publisher.objects.get_or_create(**publisher_data)
        book = Book.objects.create(publisher=publisher, **validated_data)

        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            book.authors.add(author)

        return book

    def update(self, instance: Book, validated_data: dict[str, Any]) -> Book:
        authors_data = validated_data.pop("authors", None)
        publisher_data = validated_data.pop("publisher", None)

        updated_instance = super().update(instance, validated_data)

        if publisher_data:
            publisher, _ = Publisher.objects.get_or_create(**publisher_data)
            updated_instance.publisher = publisher

        if authors_data:
            new_authors = []
            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(**author_data)
                new_authors.append(author)

            updated_instance.authors.set(new_authors)

        updated_instance.save()
        return instance
