from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import Post


@login_required(login_url=reverse_lazy("login"))
def post_list(request: HttpRequest) -> HttpResponse:
    """Список всіх постів для всіх автентифікованих користувачів."""
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", {"posts": posts})


@login_required(login_url=reverse_lazy("login"))
def create_post(request: HttpRequest) -> HttpResponse:
    """Створення посту, якщо користувач має дозвіл."""
    if not request.user.has_perm("posts.add_post"):
        raise PermissionDenied("Forbidden to create a post!")

    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")

        Post.objects.create(title=title, content=content, author=request.user)
        return redirect("post_list")

    return render(request, "posts/post_create.html")


@login_required(login_url=reverse_lazy("login"))
def edit_post(request: HttpRequest, post_id: int) -> HttpResponse:
    """Редагування свого(!) посту, якщо користувач має дозвіл."""
    if not request.user.has_perm("posts.change_post"):
        raise PermissionDenied("Forbidden to update a post!")

    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        if post.author != request.user:
            raise PermissionDenied("Only post author can edit it!")

        title = request.POST.get("title", "")
        content = request.POST.get("content", "")

        post.title = title
        post.content = content
        post.save(update_fields=["title", "content"])
        return redirect("post_list")

    return render(request, "posts/post_edit.html", {"post": post})


@login_required(login_url=reverse_lazy("login"))
def publish_post(request: HttpRequest, post_id: int) -> HttpResponse:
    """Публікація свого(!) посту, якщо користувач має дозвіл."""
    if not request.user.has_perm("posts.publish_post"):
        raise PermissionDenied("Forbidden to publish a post!")

    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)

        if post.author != request.user:
            raise PermissionDenied("Only post author can publish it!")

        post.is_published = True
        post.save(update_fields=["is_published"])
        return redirect("post_list")

    return render(request, "posts/post_publish.html")
