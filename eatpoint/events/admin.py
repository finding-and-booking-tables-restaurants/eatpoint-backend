from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, TypeEvent, EventPhoto


class PhotoInline(admin.TabularInline):
    """Админка: фото события."""

    model = EventPhoto
    extra = 0


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    """Админка: тип события."""

    list_display = ("id", "name")
    empty_value_display = "-пусто-"
    search_fields = ("name",)
    # prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка: события."""

    list_display = ("id", "name", "date_start", "establishment", "price")
    empty_value_display = "-пусто-"
    fieldsets = (
        ("Основная информация", {"fields": ("name", "establishment")}),
        ("Постер и описание", {"fields": ("image", "description")}),
        ("Начало события", {"fields": ("date_start",)}),
        ("Тип события и стоимость", {"fields": ("type_event", "price")}),
    )
    autocomplete_fields = ("type_event",)
    inlines = (PhotoInline,)

    # def preview(self, obj):
    #     """Отображение превью заведения"""
    #     if obj.image:
    #         return mark_safe(
    #             f'<img src="{obj.image.url}" style="max-height: 50px;">'
    #         )
    #     else:
    #         return "No preview"

    # preview.short_description = "Превью"
