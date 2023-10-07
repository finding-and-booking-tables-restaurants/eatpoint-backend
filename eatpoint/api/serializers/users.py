from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from users.models import User
from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField


string_validator = RegexValidator(
    r"^[a-zA-Zа-яА-Я]+$", "Имя и Фамилия должны содержать только буквы"
)


class UserSerializer(serializers.ModelSerializer):
    telephone = PhoneNumberField()
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    role = serializers.CharField()

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


class MeSerializer(serializers.ModelSerializer):
    telephone = PhoneNumberField()
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )


class SignUpSerializer(serializers.Serializer):
    telephone = PhoneNumberField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[string_validator]
    )
    role = serializers.CharField()

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

    def validate(self, data):
        email = data.get("email")
        telephone = data.get("telephone")
        if data.get("role") not in (settings.CLIENT, settings.RESTORATEUR):
            raise serializers.ValidationError(
                "Роль должна быть 'user' или 'restorateur'"
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

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    telephone = PhoneNumberField()
    confirmation_code = serializers.CharField(max_length=150)
    is_agreement = serializers.BooleanField(required=True)
    token = serializers.CharField(
        max_length=255, required=False, read_only=True
    )

    class Meta:
        model = User
        fields = ("telephone", "confirmation_code", "is_agreement", "token")

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


class CodeSerializer(serializers.ModelSerializer):
    telephone = PhoneNumberField()
    is_agreement = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("telephone", "is_agreement")

    def validate(self, data):
        telephone = data.get("telephone")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести телефон")
        return data
