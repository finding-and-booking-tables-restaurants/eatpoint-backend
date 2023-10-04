from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_admin",
        "is_active",
        "created_at",
        "updated_at",
        "confirmation_code",
        "is_agreement",
    )
    list_filter = (
        "email",
        "last_name",
    )
    search_fields = (
        "email",
        "last_name",
    )
    empty_value_display = "-пусто-"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
