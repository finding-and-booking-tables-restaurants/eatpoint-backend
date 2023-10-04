from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Establishment, Kitchen, Table, Service, File, Work


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
    list_display = (
        "name",
        "id",
        "preview",
        "email",
        "telephone",
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
