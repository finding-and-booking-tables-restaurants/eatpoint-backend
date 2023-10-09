from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from users.models import User
from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField


string_validator = RegexValidator(
    r"^[a-zA-Zа-яА-Я]+$", "Имя и Фамилия должны содержать только буквы"
)


class MyBaseSerializer(serializers.ModelSerializer):
    telephone = PhoneNumberField()
    first_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )


class UserSerializer(MyBaseSerializer):
    class Meta:
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User

    def validate(self, data):
        email = data.get("email")
        telephone = data.get("telephone")
        if data.get("role") not in (settings.CLIENT, settings.RESTORATEUR):
            raise serializers.ValidationError(
                f"Роль должна быть {settings.CLIENT} или {settings.RESTORATEUR}"
            )
        if (
            User.objects.filter(email=email).exists()
            or User.objects.filter(telephone=telephone).exists()
        ) and (
            User.objects.get(email=email).is_active
            or User.objects.get(telephone=telephone).is_active
        ):
            raise serializers.ValidationError(
                "Аккаунт с таким телефоном и/или email активирован"
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
    class Meta:
        model = User
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )


class SignUpSerializer(MyBaseSerializer):
    extra_kwargs = {"password": {"write_only": True}}

    class Meta:
        model = User
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
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
        if data.get("role") not in (settings.CLIENT, settings.RESTORATEUR):
            raise serializers.ValidationError(
                f"Роль может быть {settings.CLIENT} или {settings.RESTORATEUR}"
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
    is_agreement = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("telephone", "confirmation_code", "is_agreement")

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
    is_agreement = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("telephone", "is_agreement")

    def validate(self, data):
        telephone = data.get("telephone")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести телефон")
        return data