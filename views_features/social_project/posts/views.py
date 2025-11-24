from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CategoryForm, PostForm
from .models import Category, Post

User = get_user_model()


def debug_api(request: HttpRequest) -> JsonResponse:
    """Повертає вміст запиту в форматі JSON."""
    return JsonResponse(
        data={
            "method": request.method,
            "headers": dict(request.headers.items()),
            "params": request.GET,
            "body": request.POST,
            "cookies": request.COOKIES,
            "user": str(request.user),
        }
    )


class PostListView(LoginRequiredMixin, ListView):
    """Список всіх постів для авторизованого користувача."""

    queryset = Post.objects.select_related("author").prefetch_related("categories")
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    login_url = reverse_lazy("auth_user")


class PostDetailView(DetailView):
    """Детальна інформація про пост."""

    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"


class PostCreateView(CreateView):
    """Створення поста і призначення йому поточного користувача як автора."""

    template_name = "posts/post_form.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("post_list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Оновлення посту."""

    template_name = "posts/post_form.html"
    form_class = PostForm
    model = Post

    def form_valid(self, form) -> HttpResponseRedirect:
        form.save()
        return HttpResponseRedirect(reverse("post_list"))


class PostDeleteView(DeleteView):
    """Видалення посту."""

    model = Post
    success_url = reverse_lazy("post_list")

    def post(self, _: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        post = self.get_object()
        post.delete()
        return HttpResponseRedirect(self.success_url)


def category_list(request: HttpRequest) -> HttpResponse:
    """Отримати список категорій."""
    categories = Category.objects.all()
    return render(request, "posts/category_list.html", {"categories": categories})


def post_add_category(
    _: HttpRequest, post_id: int, category_id: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    """Додати категорію до поста."""
    post = get_object_or_404(Post, pk=post_id)
    category = get_object_or_404(Category, pk=category_id)

    post.categories.add(category)
    return redirect("post_list")


def post_remove_category(
    _: HttpRequest, post_id: int, category_id: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    """Видалити категорію із поста."""
    post = get_object_or_404(Post, pk=post_id)
    category = get_object_or_404(Category, pk=category_id)

    post.categories.remove(category)
    return redirect("post_list")


@login_required(login_url=reverse_lazy("auth_user"))
def category_create(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Створити категорію."""
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("category_list")

    return render(request, "posts/category_form.html", {"form": form})


@require_POST
def category_remove(
    _: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    """Видалити категорію."""
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("category_list")


def category_update(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponse:
    """Оновити категорію."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    return render(request, "posts/category_form.html", {"form": form})


def category_update_or_create(request: HttpRequest) -> HttpResponse:
    """Оновити або створити категорію, якщо не існує."""
    category, created = Category.objects.update_or_create(
        title="Tutorial", defaults={"description": "Updated or created"}
    )
    return render(
        request,
        "posts/get_or_create_result.html",
        {"category": category, "created": created},
    )


def category_get_or_create(request: HttpRequest) -> HttpResponse:
    """Отримати категорію або створити, якщо не існує."""
    category, created = Category.objects.get_or_create(
        title="Default category", defaults={"description": "Auto-created if not exists"}
    )
    return render(
        request,
        "posts/get_or_create_result.html",
        {"category": category, "created": created},
    )
