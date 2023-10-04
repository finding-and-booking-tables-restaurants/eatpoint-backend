from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telephone, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(telephone=telephone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, telephone, email=None, password=None, **extra_fields
    ):
        if not telephone:
            raise ValueError("Необходимо ввести телефон")
        if not email:
            raise ValueError("Необходимо ввести email")
        if not extra_fields.get("first_name", None):
            raise ValueError("Необходимо ввести first_name")
        if not extra_fields.get("last_name", None):
            raise ValueError("Необходимо ввести last_name")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(telephone, email, password, **extra_fields)

    def create_superuser(
        self, telephone, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(telephone, email, password, **extra_fields)
