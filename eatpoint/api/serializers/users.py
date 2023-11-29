from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import core.constants
from core.validators import string_validator
from users.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class MyBaseSerializer(serializers.ModelSerializer):
    """
    Абстрактный базовый сериализатор данных пользователя.
    """

    telephone = PhoneNumberField()
    email = serializers.EmailField()
    first_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )


class UserSerializer(MyBaseSerializer):
    """
    Сериализатор данных пользователя.
    """

    class Meta:
        model = User
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )

    def validate(self, data):
        email = data.get("email")
        telephone = data.get("telephone")
        user_with_email = User.objects.filter(email=email)
        user_with_telephone = User.objects.filter(telephone=telephone)
        if data.get("role") not in (
            core.constants.CLIENT,
            core.constants.RESTORATEUR,
        ):
            raise serializers.ValidationError(
                f"Роль должна быть {core.constants.CLIENT} или {core.constants.RESTORATEUR}"
            )
        if (user_with_email.exists() or user_with_telephone.exists()) and (
            user_with_email[0].is_active or user_with_telephone[0].is_active
        ):
            raise serializers.ValidationError(
                "Аккаунт с таким телефоном и/или email уже активирован"
            )
        if (
            telephone is not None
            and User.objects.get(telephone=telephone) == "me"
        ):
            raise serializers.ValidationError(
                f"Номер {telephone} уже зарезервирован!"
            )
        return data


class MeSerializer(MyBaseSerializer):
    """
    Сериализатор собственных данных пользователя.
    """

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        extra_kwargs = {
            "email": {"required": False},
            "telephone": {"required": False},
        }

    def validate_email(self, email):
        user = self.instance
        if user and user.email == email:
            return email

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise ValidationError("Email уже зарезервирован!")
        return email

    def validate_telephone(self, telephone):
        user = self.instance
        if user and user.telephone == telephone:
            return telephone

        if (
            User.objects.filter(telephone=telephone)
            .exclude(id=user.id)
            .exists()
        ):
            raise ValidationError("Email уже зарезервирован!")
        return telephone


class SignUpSerializer(MyBaseSerializer):
    """
    Сериализатор данных для регистрации пользователя.
    """

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            "telephone",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "is_agreement",
            "confirm_code_send_method",
        )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        email = data.get("email")
        telephone = data.get("telephone")
        if data.get("confirm_code_send_method") not in (
            core.constants.EMAIL,
            core.constants.SMS,
            core.constants.TELEGRAM,
            core.constants.NOTHING,
        ):
            raise serializers.ValidationError(
                f"Метод отправки кода может быть {core.constants.EMAIL} "
                f"или {core.constants.SMS} или {core.constants.TELEGRAM} "
                f"или {core.constants.NOTHING}"
            )

        # =========== Нужно убрать если включим отправку по SMTP и другой способ ======
        if data.get("confirm_code_send_method") in (
            # core.constants.EMAIL,
            core.constants.SMS,
            # core.constants.TELEGRAM,
        ):
            raise serializers.ValidationError(
                f"Способ отправки кода '{data.get('confirm_code_send_method')}' "
                f"отключен... "
                f"укажите метод '{core.constants.NOTHING}'"
            )
        # ============================================================================

        if data.get("role") not in (
            core.constants.CLIENT,
            core.constants.RESTORATEUR,
        ):
            raise serializers.ValidationError(
                f"Роль может быть {core.constants.CLIENT} или {core.constants.RESTORATEUR}"
            )
        if not User.objects.filter(telephone=telephone, email=email).exists():
            if (
                User.objects.filter(email=email).exists()
                or User.objects.filter(telephone=telephone).exists()
            ):
                raise serializers.ValidationError(
                    "Пользователь с таким email или phone уже активирован..."
                )
        return data

    def validate_password(self, value):
        validate_password(value)
        return value


class ConfirmCodeSerializer(MyBaseSerializer):
    """
    Сериализатор данных для подтверждения регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ("telephone", "confirmation_code")

    def validate(self, data):
        telephone = data.get("telephone")
        confirmation_code = data.get("confirmation_code")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести телефон")
        if confirmation_code is None:
            raise serializers.ValidationError(
                "Необходимо ввести 6-ти значный код из эл.почты"
            )
        return data


class ConfirmCodeRefreshSerializer(MyBaseSerializer):
    """
    Сериализатор данных для обновления кода подтверждения при регистрации.
    """

    class Meta:
        model = User
        fields = ("telephone",)

    def validate(self, data):
        telephone = data.get("telephone")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести телефон")
        return data
