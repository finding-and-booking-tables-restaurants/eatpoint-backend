from rest_framework import serializers

from users.models import ROLE_CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User

    def validate(self, data):
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегистрирован..."
            )
        return data


class MeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, required=False, read_only=True
    )

    class Meta:
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        email = data.get("email")
        if not User.objects.filter(email=email).exists():
            return data

        user = User.objects.get(email=email)
        if user.is_active:
            raise serializers.ValidationError(
                "Пользователь с таким email уже активирован..."
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    confirmation_code = serializers.CharField(
        max_length=6,
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
