from django.contrib import admin

from .models import Event, TypeEvent, Reccurence


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    """Админка: тип события."""

    list_display = ("id", "name")
    empty_value_display = "-пусто-"
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка: события."""

    list_display = ("id", "name", "date_start", "establishment", "price")
    empty_value_display = "-пусто-"
    fieldsets = (
        ("Основная информация", {"fields": ("name", "establishment")}),
        ("Постер и описание", {"fields": ("cover_image", "description")}),
        ("Начало события", {"fields": ("date_start",)}),
        ("Тип события и стоимость", {"fields": ("type_event", "price")}),
    )
    autocomplete_fields = ("type_event",)


@admin.register(Reccurence)
class ReccurenceAdmin(admin.ModelAdmin):
    """Админка: повторы событий."""

    list_display = ("id", "description", "days")
    empty_value_display = "-пусто-"
