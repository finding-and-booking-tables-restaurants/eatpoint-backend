from datetime import datetime, timedelta
import random

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .usermanager import UserManager

USER = "user"
RESTAURATEUR = "restaurateur"
MODERATOR = "moderator"
ADMIN = "admin"
SUPERUSER = "superuser"

ROLE_CHOICES = (
    (USER, "Пользователь"),
    (RESTAURATEUR, "Ресторатор"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
    (SUPERUSER, "Суперюзер"),
)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Адрес эл.почты",
        max_length=254,
        db_index=True,
        unique=True,
    )

    first_name = models.CharField(
        "Имя",
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=True,
    )

    role = models.CharField(
        "Роль пользователя",
        max_length=20,
        default=USER,
        choices=ROLE_CHOICES,
    )

    confirmation_code = models.CharField(
        "Код подтверждения",
        max_length=6,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_restaurateur(self):
        return self.role == RESTAURATEUR

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_administrator(self):
        return self.role == ADMIN

    @property
    def is_superuser(self):
        return self.role == SUPERUSER

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def confirm_code(self):
        return self._generate_confirm_code()

    @staticmethod
    def _generate_confirm_code():
        random.seed()
        return str(random.randint(100000, 999999))

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
