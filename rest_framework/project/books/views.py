from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from .models import Book
from .serializers import BookSerializer


class BookListCreateAPIView(APIView):
    """View для створення книги і для отримання списку книг."""

    def get(self, _: Request) -> Response:
        books = Book.objects.select_related("publisher").prefetch_related("authors")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
