from django.contrib import admin, messages
from django.core import serializers
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from .models import Article, Category

# реєстрація моделей в адмінці через decorator замість admin.site.register
# це сучасніший підхід і зручніше для великих проектів
# admin.site.register([Article, Category])


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1  # кількість додаткових порожніх форм для створення нових статей
    max_num = 5  # максимальна кількість інлайн-статей на категорію


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
    )  # показуємо назву та дату створення категорії у списку
    search_fields = ("title",)  # дозволяє шукати категорії за назвою
    inlines = (ArticleInline,)  # показуємо пов’язані статті прямо на сторінці категорії


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # оптимізація запитів: одразу підтягуємо категорію для list_display
    list_select_related = ("category",)

    # поля, які будуть показані у списку статей
    list_display = (
        "title",
        "category",
        "published_status",  # користувацьке поле через @admin.display
        "is_published",
        "short_content",  # користувацьке поле через @admin.display
        "created_at",
    )

    # групування полів на сторінці редагування
    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("title", "slug", "category")},
        ),
        ("Контент", {"fields": ("content",)}),
        (
            "Публікація",
            {
                "fields": ("is_published", "created_at"),
                "classes": ["collapse"],  # ця секція буде схована за замовчуванням
            },
        ),
    )

    # фільтри в сайдбарі для швидкого сортування
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "content")  # пошук по назві та контенту
    search_help_text = "ПОШУК ЗА НАЗВОЮ ТА КОНТЕНТОМ"  # пояснення для користувача
    ordering = ("-created_at", "title")  # сортування за датою (спадання) та назвою
    readonly_fields = ("created_at",)  # не редагується вручну
    date_hierarchy = "created_at"  # навігація по даті створення

    # дозволяємо редагувати поле прямо у списку, але не перше у list_display
    list_editable = ("is_published",)

    # автоматичне заповнення slug при створенні на основі title
    prepopulated_fields = {"slug": ("title",)}

    actions = ("publish_articles", "export_as_json")  # дії для списку статей
    save_on_top = True  # кнопки збереження також зверху форми

    @admin.display(description="Статус", boolean=True, ordering="is_published")
    def published_status(self, obj: Article) -> bool:
        """Показуємо в списку, чи опублікована стаття."""
        return obj.is_published

    @admin.display(description="Короткий текст")
    def short_content(self, obj: Article) -> str:
        """Показуємо перші 40 символів контенту."""
        return obj.content[:40] + "..."

    @admin.action(description="Опублікувати вибрані статті")
    def publish_articles(
        self, request: HttpRequest, queryset: QuerySet[Article]
    ) -> None:
        """Масова дія: ставимо is_published=True для вибраних статей."""
        updated_number = queryset.update(is_published=True)
        self.message_user(
            request,
            f"{updated_number} story(ies) was successfully marked as published.",
            messages.SUCCESS,
        )

    @admin.action(description="Експорт вибраних статей в JSON формат")
    def export_as_json(
        self, request: HttpRequest, queryset: QuerySet[Article]
    ) -> HttpResponse:
        """Масова дія: експорт вибраних статей у JSON-файл."""
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = "attachment; filename=articles.json"
        serializers.serialize("json", queryset, stream=response)
        return response
