from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("username", "email")
    search_fields = ("username", "email")
    empty_value_display = "-пусто-"
