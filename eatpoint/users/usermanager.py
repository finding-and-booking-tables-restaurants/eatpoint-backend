from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер пользователя."""

    use_in_migrations = True

    def create_user(self, telephone, email, password, role, **extra_fields):
        """Метод для создания пользователя."""
        if not telephone:
            raise ValueError("Необходимо ввести телефон")
        if not email:
            raise ValueError("Необходимо ввести email")
        if not role:
            raise ValueError("Необходимо ввести role")
        if not extra_fields.get("first_name", None):
            raise ValueError("Необходимо ввести first_name")
        if not extra_fields.get("last_name", None):
            raise ValueError("Необходимо ввести last_name")

        email = self.normalize_email(email)
        user = self.model(telephone, email, role, **extra_fields)
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Метод для создания суперпользователя."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user
