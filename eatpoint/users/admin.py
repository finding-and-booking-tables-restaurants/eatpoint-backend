from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "telephone",
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
        "confirm_code_send_method",
    )
    list_filter = (
        "role",
        "email",
        "last_name",
        "is_active",
        "is_agreement",
    )
    search_fields = (
        "email",
        "last_name",
    )
    empty_value_display = "-пусто-"
