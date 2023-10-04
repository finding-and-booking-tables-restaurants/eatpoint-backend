from django.core.validators import RegexValidator
from rest_framework import serializers
from users.models import User
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    telephone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Неверный формат номера",
            )
        ],
        max_length=17,
    )
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(
        choices=settings.ROLE_CHOICES, required=False
    )

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
    telephone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Неверный формат номера",
            )
        ],
        max_length=17,
    )
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(
        choices=settings.ROLE_CHOICES, required=False, read_only=True
    )

    class Meta:
        fields = (
            "telephone",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    telephone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Неверный формат номера",
            )
        ],
        max_length=17,
    )
    password = serializers.CharField(max_length=254)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate(self, data):
        email = data.get("email")
        telephone = data.get("telephone")
        if not User.objects.filter(telephone=telephone, email=email).exists():
            if (
                User.objects.filter(email=email).exists()
                or User.objects.filter(telephone=telephone).exists()
            ):
                raise serializers.ValidationError(
                    "Пользователь с таким email или phone уже активирован..."
                )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    telephone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Неверный формат номера",
            )
        ],
        max_length=17,
    )
    confirmation_code = serializers.CharField(max_length=150)
    is_agreement = serializers.BooleanField(required=True)
    token = serializers.CharField(
        max_length=255, required=False, read_only=True
    )

    class Meta:
        fields = ("telephone", "confirmation_code", "is_agreement", "token")
        model = User

    def validate(self, data):
        telephone = data.get("telephone")
        confirmation_code = data.get("confirmation_code")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести телефон")
        if confirmation_code is None:
            raise serializers.ValidationError(
                "Необходимо ввести 6-ти значный код из эл.почты/sms"
            )
        return data
