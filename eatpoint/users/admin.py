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
        "is_active",
        "created_at",
        "updated_at",
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
