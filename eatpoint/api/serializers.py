from django.core.validators import RegexValidator
from rest_framework import serializers
from users.models import ROLE_CHOICES, User


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
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

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
        ):
            raise serializers.ValidationError(
                "А Вы точно зедсь первый раз?!"
                "Я точно помню, что такие telephone и/или email уже видел :)"
            )
        if telephone is not None and telephone.lower() == "me":
            raise serializers.ValidationError(
                f"telephone {telephone} зарезервировано!"
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
        choices=ROLE_CHOICES, required=False, read_only=True
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
                    "А Вы точно зедсь первый раз?!"
                    "Я точно помню, что такие username и/или email уже видел!"
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
    confirmation_code = serializers.CharField(
        max_length=150,
    )
    token = serializers.CharField(
        max_length=255, required=False, read_only=True
    )

    class Meta:
        fields = ("telephone", "confirmation_code", "token")
        model = User

    def validate(self, data):
        telephone = data.get("telephone")
        confirmation_code = data.get("confirmation_code")
        if telephone is None:
            raise serializers.ValidationError("Необходимо ввести telephone")
        if confirmation_code is None:
            raise serializers.ValidationError(
                "Необходимо ввести присланный confirmation code"
            )
        return data
