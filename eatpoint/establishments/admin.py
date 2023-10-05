from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Establishment, Kitchen, Table, Service, File, Work


class ContactForm(forms.ModelForm):
    class Meta:
        widgets = {
            "telephone": PhoneNumberPrefixWidget(initial="RU"),
        }


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start", "end")
    empty_value_display = "-пусто-"


@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "slug")
    empty_value_display = "-пусто-"


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "slug")
    empty_value_display = "-пусто-"


@admin.register(File)
class File(admin.ModelAdmin):
    list_display = ("image",)
    empty_value_display = "-пусто-"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "slug")
    empty_value_display = "-пусто-"


class TablesInLine(admin.TabularInline):
    model = Establishment.tables.through


class WorkInLine(admin.TabularInline):
    model = Establishment.worked.through


class FileInLine(admin.TabularInline):
    model = Establishment.file.through


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
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
    inlines = (
        TablesInLine,
        FileInLine,
        WorkInLine,
    )

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.poster.url}" style="max-height: 50px;">'
        )
