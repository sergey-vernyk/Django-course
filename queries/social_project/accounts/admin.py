from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "birth_date",
        "first_name",
        "last_name",
        "gender",
        "country",
    )
    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        (
            "Personal info",
            {"fields": ["first_name", "last_name", "birth_date", "gender"]},
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "birth_date", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
