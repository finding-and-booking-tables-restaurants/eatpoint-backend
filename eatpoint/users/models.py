import random

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import SEND_CONFIRM_CODE_METHOD, ROLE_CHOICES
from core.constants import (
    CLIENT,
    RESTORATEUR,
    ADMINISTRATOR,
    MIN_LIMIT_CONFIRM_CODE,
    MAX_LIMIT_CONFIRM_CODE,
)
from .usermanager import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    """Модель пользователя."""

    telephone = PhoneNumberField(unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=50,
        db_index=True,
        unique=True,
    )

    first_name = models.CharField(
        "First name",
        max_length=150,
    )
    last_name = models.CharField(
        "Last name",
        max_length=150,
    )

    role = models.CharField(
        "User`s role",
        max_length=25,
        choices=ROLE_CHOICES,
    )

    confirmation_code = models.CharField(
        "Confirmation code",
        max_length=150,
        blank=True,
    )

    confirm_code_send_method = models.CharField(
        "Способ отправки кода подтверждения",
        max_length=10,
        choices=SEND_CONFIRM_CODE_METHOD,
    )

    is_agreement = models.BooleanField("Agreement", default=False)
    is_active = models.BooleanField("Active", default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("telephone", "email"), name="phone_email_unique"
            )
        ]

    def __str__(self):
        return self.email

    @property
    def is_client(self):
        return self.role == CLIENT

    @property
    def is_restorateur(self):
        return self.role == RESTORATEUR

    @property
    def is_administrator(self):
        return self.role == ADMINISTRATOR

    @property
    def confirm_code(self):
        return self._generate_confirm_code()

    @staticmethod
    def _generate_confirm_code():
        random.seed()
        return str(
            random.randint(
                MIN_LIMIT_CONFIRM_CODE,
                MAX_LIMIT_CONFIRM_CODE,
            )
        )
