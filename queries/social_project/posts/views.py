from django.contrib.auth import get_user_model
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, PostForm
from .models import Category, Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("author").prefetch_related("categories")
    return render(request, "posts/post_list.html", context={"posts": posts})


def post_create(request: HttpRequest):
    form = PostForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        return redirect("post_list")

    return render(request, "posts/post_form.html", context={"form": form})
