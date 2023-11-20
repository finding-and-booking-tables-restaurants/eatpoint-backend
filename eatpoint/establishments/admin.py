from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import (
    Establishment,
    Kitchen,
    OwnerResponse, Service,
    Event,
    Review,
    TypeEst,
    ZoneEstablishment,
    ImageEstablishment,
    WorkEstablishment,
    SocialEstablishment,
    Favorite,
    City,
    TypeEvents,
)


class ContactForm(forms.ModelForm):
    """Виджет для выбора кода региона"""

    class Meta:
        widgets = {
            "telephone": PhoneNumberPrefixWidget(initial="RU"),
        }


@admin.register(ZoneEstablishment)
class ZoneAdmin(admin.ModelAdmin):
    """Админка: зона заведения"""

    list_display = ("zone", "id")


@admin.register(ImageEstablishment)
class ImageEstablishmentAdmin(admin.ModelAdmin):
    """Админка: отзывы"""

    list_display = ("id", "name")


@admin.register(OwnerResponse)
class OwnerResponseAdmin(admin.ModelAdmin):
    """Админка: ответ владельца заведения"""

    list_display = ("id", "establishment_owner", "review", "text", "created")
    list_filter = ("establishment_owner", "created")
    search_fields = ("text",)


class OwnerResponseInline(admin.TabularInline):
    """Админка: управление OwnerResponse внутри панели Review"""

    model = OwnerResponse
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка: отзывы"""

    list_display = ("id", "author", "establishment")
    inlines = [OwnerResponseInline]


@admin.register(TypeEvents)
class TypeEventAdmin(admin.ModelAdmin):
    """Админка: события"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


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


@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    """Админка: кухня"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка: город"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    search_fields = ("name",)


@admin.register(TypeEst)
class TypeAdmin(admin.ModelAdmin):
    """Админка: тип заведения"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка: доп. услуги"""

    list_display = ("name", "id")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка: избранное"""

    list_display = (
        "id",
        "user",
        "establishment",
    )
    search_fields = (
        "user__email",
        "establishment__name",
    )


class ZonesInLine(admin.TabularInline):
    """Админка: добавление зоны заведения"""

    model = ZoneEstablishment


class SocialInLine(admin.TabularInline):
    """Админка: добавление соц. сетей"""

    model = SocialEstablishment


class ImageInLine(admin.TabularInline):
    """Админка: добавление изображений"""

    model = ImageEstablishment


class WorkInLine(admin.TabularInline):
    """Админка: добавление времени работы"""

    model = WorkEstablishment


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    """Админка: заведение"""

    form = ContactForm
    list_display = (
        "name",
        "id",
        "preview",
        "email",
        "is_verified",
    )
    fieldsets = (
        ("Основная информация", {"fields": ("owner", "name", "poster")}),
        ("Верификация", {"fields": ("is_verified",)}),
        (
            "Контакты и адреса",
            {"fields": ("cities", "address", "telephone", "email")},
        ),
        (
            "Кухни, типы, сервисы",
            {"fields": ("types", "kitchens", "services")},
        ),
        (
            "Средний чек и описание",
            {"fields": ("average_check", "description")},
        ),
        ("Координаты", {"fields": ("latitude", "longitude")}),
    )
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    inlines = (ZonesInLine, WorkInLine, ImageInLine, SocialInLine)
    autocomplete_fields = ["cities"]

    def preview(self, obj):
        """Отображение превью заведения"""
        if obj.poster:
            return mark_safe(
                f'<img src="{obj.poster.url}" style="max-height: 50px;">'
            )
        else:
            return "No preview"

    preview.short_description = "Превью"
