from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, TypeEvent


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    """Админка: события"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    # prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка: события"""

    list_display = ("name", "preview", "id", "date_start")
    empty_value_display = "-пусто-"
    fieldsets = (
        ("Основная информация", {"fields": ("name", "establishment")}),
        ("Постер и описание", {"fields": ("image", "description")}),
        ("Начало и конец события", {"fields": ("date_start", "date_end")}),
        ("Тип события и стоимость", {"fields": ("type_event", "price")}),
    )

    def preview(self, obj):
        """Отображение превью заведения"""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 50px;">'
            )
        else:
            return "No preview"

    preview.short_description = "Превью"
