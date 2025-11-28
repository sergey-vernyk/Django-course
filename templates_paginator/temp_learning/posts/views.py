from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def post_list(request: HttpRequest) -> HttpResponse:
    """Отримання списку всіх постів."""
    posts = Post.objects.select_related("author", "category").order_by("-created_at")
    categories = Category.objects.all()

    return render(
        request,
        "posts/post_list.html",
        {
            "posts": posts,
            "categories": categories,
        },
    )


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Отримання інформації по пост."""
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "posts/post_detail.html", {"post": post})


def category_list(request: HttpRequest) -> HttpResponse:
    """Отримання списку категорій."""
    categories = Category.objects.all()
    return render(request, "posts/category_list.html", {"categories": categories})
