from django.contrib import admin

from .models import Article, Category

# admin.site.register([Article, Category])


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1
    max_num = 5


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
    inlines = (ArticleInline,)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_published",
        "published_status",
        "short_content",
        "created_at",
    )
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "content")
    search_help_text = "ПОШУК ЗА НАЗВОЮ ТА КОНТЕНТОМ"

    ordering = ("-created_at", "title")
    date_hierarchy = "created_at"
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True

    @admin.display(description="Статус", boolean=True, ordering="is_published")
    def published_status(self, obj: Article) -> bool:
        return obj.is_published

    @admin.display(description="Короткий текст")
    def short_content(self, obj: Article) -> str:
        return obj.content[:40] + "..."
