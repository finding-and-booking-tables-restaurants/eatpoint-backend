from django.core.validators import RegexValidator
from rest_framework import serializers

from users.models import ROLE_CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+",
                message="Используйте допустимые символы в username",
            )
        ],
    )
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        if (
            User.objects.filter(email=email).exists()
            or User.objects.filter(username=username).exists()
        ):
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегистрирован..."
            )
        if username is not None and username.lower() == "me":
            raise serializers.ValidationError(
                f"username {username} зарезервировано!"
            )
        return data


class MeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+",
                message="Используйте допустимые символы в username",
            )
        ],
    )
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, required=False, read_only=True
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+",
                message="Используйте допустимые символы в username",
            )
        ],
    )
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        if not User.objects.filter(username=username, email=email).exists():
            if (
                User.objects.filter(email=email).exists()
                or User.objects.filter(username=username).exists()
            ):
                raise serializers.ValidationError(
                    "Пользователь с таким email уже зарегистрирован..."
                )
        if username is not None and username.lower() == "me":
            raise serializers.ValidationError(
                f"Имя {username} зарезервировано!"
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(
        max_length=150,
    )
    token = serializers.CharField(
        max_length=255, required=False, read_only=True
    )

    class Meta:
        fields = ("email", "confirmation_code", "token")
        model = User

    def validate(self, data):
        email = data.get("email")
        confirmation_code = data.get("confirmation_code")
        if email is None:
            raise serializers.ValidationError("Необходимо ввести email")
        if confirmation_code is None:
            raise serializers.ValidationError(
                "Необходимо ввести 6-ти значный код из эл.почты"
            )
        return data
