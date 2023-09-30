from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, role="user"):
        if not email:
            raise ValueError("Необходимо ввести email")

        user = self.model(
            email=self.normalize_email(email),
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, role="superuser")
        user.is_admin = True
        user.save(using=self._db)
        return user
