from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import Project


@login_required(login_url=reverse_lazy("login"))
def get_users_projects(request: HttpRequest) -> HttpResponse:
    """Показує проєкти користувача. Дані дістаються з кешу."""
    user = request.user
    cache_key = f"user:{user.pk}:project"

    projects = cache.get(cache_key)

    if projects is None:
        projects = list(Project.objects.filter(users=user))
        cache.set(cache_key, projects)

    return render(
        request,
        "django_signals/user_projects.html",
        {"projects": projects},
    )


@login_required(login_url=reverse_lazy("login"))
def add_user_to_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    Додає поточного користувача до проєкту.
    Інвалідація кешу проходить не тут, а в сигналі.
    """
    project = get_object_or_404(Project, id=project_id)
    project.users.add(request.user)
    return redirect("user-projects")


@login_required(login_url=reverse_lazy("login"))
def remove_user_from_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """Видаляє користувача з проєкту."""
    project = get_object_or_404(Project, id=project_id)
    project.users.remove(request.user)
    return redirect("user-projects")


@login_required(login_url=reverse_lazy("login"))
def clear_user_projects(request: HttpRequest) -> HttpResponse:
    """Очищає всі m2m-зв'язки користувача."""
    request.user.project.clear()

    return redirect("user-projects")
