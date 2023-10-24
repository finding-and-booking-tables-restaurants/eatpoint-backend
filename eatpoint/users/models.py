from datetime import datetime, timedelta
import random

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

import core.choices
import core.constants
from .usermanager import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    """Модель пользователя."""

    telephone = PhoneNumberField(unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=254,
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
        choices=core.choices.ROLE_CHOICES,
    )

    confirmation_code = models.CharField(
        "Confirmation code",
        max_length=150,
        blank=True,
    )

    confirm_code_send_method = models.CharField(
        "Способ отправки кода подтверждения",
        max_length=10,
        choices=core.choices.SEND_CONFIRM_CODE_METHOD,
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

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_client(self):
        return self.role == core.constants.CLIENT

    @property
    def is_restorateur(self):
        return self.role == core.constants.RESTORATEUR

    @property
    def is_administrator(self):
        return self.role == core.constants.ADMINISTRATOR

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def confirm_code(self):
        return self._generate_confirm_code()

    @staticmethod
    def _generate_confirm_code():
        random.seed()
        return str(
            random.randint(
                core.constants.MIN_LIMIT_CONFIRM_CODE,
                core.constants.MAX_LIMIT_CONFIRM_CODE,
            )
        )

    def _generate_jwt_token(self):
        dt = datetime.now()
        td = timedelta(days=1)
        payload = self.pk
        token = jwt.encode(
            {
                "user_id": payload,
                "exp": int((dt + td).timestamp()),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token
