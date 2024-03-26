from django.contrib import admin

from reviews.models import OwnerResponse, Review


@admin.register(OwnerResponse)
class OwnerResponseAdmin(admin.ModelAdmin):
    """Админка: ответ владельца заведения"""

    list_display = ("review", "id", "created")
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
