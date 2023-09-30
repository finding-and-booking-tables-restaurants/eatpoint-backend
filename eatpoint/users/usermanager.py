from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, telephone, email, password, role, first_name, last_name
    ):
        if not telephone:
            raise ValueError("Необходимо ввести телефон")
        if not email:
            raise ValueError("Необходимо ввести email")
        if not first_name:
            raise ValueError("Необходимо ввести first_name")
        if not last_name:
            raise ValueError("Необходимо ввести last_name")

        user = self.model(
            email=self.normalize_email(email),
            telephone=telephone,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            telephone=99999999,
            role="superuser",
            first_name="superuser",
            last_name="superuser",
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
