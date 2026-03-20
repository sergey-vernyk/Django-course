from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Author, Book, Publisher

GET_LIST_CREATE_BOOK_URL = reverse("book_list_create")


class BookAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.publisher = Publisher.objects.create(
            name="Test Publisher", website="https://test.com"
        )

        self.author = Author.objects.create(
            first_name="John", last_name="Doe", email="john@example.com"
        )

        self.book = Book.objects.create(
            title="Test Book",
            publisher=self.publisher,
            publication_date="2026-01-01",
            pages=200,
        )

        self.book.authors.add(self.author)

        self.valid_payload = {
            "title": "Python for Teens",
            "publication_date": "2026-02-01",
            "pages": 350,
            "publisher": {
                "name": "New TeenBooks Publishing",
                "website": "https://newteenbooks.example.com",
            },
            "authors": [
                {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
                {
                    "first_name": "Alice",
                    "last_name": "Wonder",
                    "email": "alice@example.com",
                },
            ],
        }

        self.invalid_payload = {"title": "", "pages": "abc"}

    def test_get_books_list(self) -> None:
        response = self.client.get(GET_LIST_CREATE_BOOK_URL)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_success(self) -> None:
        response = self.client.post(
            GET_LIST_CREATE_BOOK_URL, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_book = Book.objects.filter(title=self.valid_payload["title"]).first()
        self.assertIsNotNone(created_book)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_invalid_payload(self) -> None:
        response = self.client.post(
            GET_LIST_CREATE_BOOK_URL,
            self.invalid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)
