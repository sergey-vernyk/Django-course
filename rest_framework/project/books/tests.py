from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from rest_framework import status

from .models import Author, Book, Publisher

GET_LIST_CREATE_BOOK_URL = reverse("book_list_create")


class BookAPITestCase(APITestCase):
    def setUp(self) -> None:
        # базові пов'язані об'єкти для тестів
        self.publisher = Publisher.objects.create(
            name="Test Publisher", website="https://test.com"
        )

        self.author = Author.objects.create(
            first_name="John", last_name="Doe", email="john@example.com"
        )

        # початкова книга для GET / UPDATE / DELETE тестів
        self.book = Book.objects.create(
            title="Test Book",
            publisher=self.publisher,
            publication_date="2026-01-01",
            pages=200,
        )

        self.book.authors.add(self.author)

        # валідний payload для create/update
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

        # не валідні дані для negative test
        self.invalid_payload = {"title": "", "pages": "abc"}

    def test_get_books_list(self) -> None:
        # перевірка списку книг
        response = self.client.get(GET_LIST_CREATE_BOOK_URL)

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_success(self) -> None:
        # успішне створення книги
        response = self.client.post(
            GET_LIST_CREATE_BOOK_URL, self.valid_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_book = Book.objects.filter(title=self.valid_payload["title"]).first()
        self.assertIsNotNone(created_book)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_invalid_payload(self) -> None:
        # create з помилковими даними
        response = self.client.post(
            GET_LIST_CREATE_BOOK_URL,
            self.invalid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)

    def test_get_single_book(self) -> None:
        # отримання конкретної книги
        get_book_url = reverse("book_detail", kwargs={"pk": self.book.pk})
        response = self.client.get(get_book_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk), self.book)

    def test_get_single_book_not_found(self) -> None:
        # книга не існує
        get_book_url = reverse("book_detail", kwargs={"pk": 999})
        response = self.client.get(get_book_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book_put(self) -> None:
        # повне оновлення книги
        payload = self.valid_payload.copy()
        payload["title"] = "Updated Title"

        update_book_url = reverse("book_detail", kwargs={"pk": self.book.pk})
        response = self.client.put(update_book_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Book.objects.get(title=payload["title"]).title,
            "Updated Title",
        )

    def test_partial_update_book_patch(self) -> None:
        # часткове оновлення одного поля
        update_book_url = reverse("book_detail", kwargs={"pk": self.book.pk})
        response = self.client.patch(update_book_url, {"pages": 500}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk).pages, 500)

    def test_delete_book(self) -> None:
        # видалення книги
        delete_book_url = reverse("book_detail", kwargs={"pk": self.book.pk})
        response = self.client.delete(delete_book_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

        deleted_book = Book.objects.filter(title=self.book.title).first()
        self.assertIsNone(deleted_book)
