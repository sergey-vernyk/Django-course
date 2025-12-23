from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # 1. Демонстрація low-level cache (cache.get / cache.set)
    path("slow/", views.slow_view, name="slow"),
    # 2. Кешування даних (users list)
    path("users/", views.users_view, name="users"),
    # # 3. Кешування всієї сторінки (@cache_page)
    path("", views.homepage, name="home"),
    # # 4. Інвалідація кешу (створення користувача)
    path("create-user/", views.create_user, name="create_user"),
]
