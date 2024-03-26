import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from string import ascii_letters, digits, punctuation


class NoRussianLettersValidator(object):

    """Пароль не должен содержать букв русского алфавита."""

    def validate(self, password, user=None):
        if re.findall("[а-яА-я]", password):
            raise ValidationError(
                _("Пароль не должен содержать букв русского алфавита"),
                code="password_no_russian_letters",
            )

    def get_help_text(self):
        return _("Пароль не должен содержать букв русского алфавита.")


class OnlyAllowedCharactersValidator(object):
    def validate(self, password, user=None):
        allowed_characters = ascii_letters + digits + punctuation
        if any(char not in allowed_characters for char in password):
            raise ValidationError(
                _(
                    f"Пароль может содержать только {ascii_letters}, {digits} и {punctuation}."
                ),
                code="password_invalid_characters",
            )

    def get_help_text(self):
        return _(
            f"Пароль может содержать только {ascii_letters}, {digits} и {punctuation}."
        )


class MaximumLengthValidator:
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f"пароль должен быть не более {self.max_length} символов."),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _(f"пароль должен быть не более {self.max_length} символов.")
