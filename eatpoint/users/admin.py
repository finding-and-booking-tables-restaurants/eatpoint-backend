from django.contrib import admin
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import User


class ContactForm(forms.ModelForm):
    class Meta:
        widgets = {
            "telephone": PhoneNumberPrefixWidget(initial="RU"),
        }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = ContactForm
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
