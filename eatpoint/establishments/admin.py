from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import (
    Establishment,
    Kitchen,
    Service,
    Event,
    Review,
    TypeEst,
    ZoneEstablishment,
    ImageEstablishment,
    WorkEstablishment,
    SocialEstablishment,
    Favorite,
    City,
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

    list_display = ("id",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка: отзывы"""

    list_display = ("id",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка: события"""

    list_display = ("id",)
    empty_value_display = "-пусто-"


@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    """Админка: кухня"""

    list_display = ("id", "name", "description", "slug")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка: город"""

    list_display = ("id", "name", "slug")
    empty_value_display = "-пусто-"
    search_fields = ("name",)


@admin.register(TypeEst)
class TypeAdmin(admin.ModelAdmin):
    """Админка: тип заведения"""

    list_display = ("id", "name", "description", "slug")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка: доп. услуги"""

    list_display = ("id", "name", "description", "slug")
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
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    inlines = (ZonesInLine, WorkInLine, ImageInLine, SocialInLine)
    autocomplete_fields = ["cities"]

    def preview(self, obj):
        """Отображение превью заведения"""
        return mark_safe(
            f'<img src="{obj.poster.url}" style="max-height: 50px;">'
        )

    preview.short_description = "Превью"
