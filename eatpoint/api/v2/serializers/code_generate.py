from rest_framework import serializers


class SMSSendSerializer(serializers.Serializer):
    """Сериализатор отправки кода"""

    email = serializers.EmailField(max_length=50, required=True)


class SMSVerifySerializer(serializers.Serializer):
    """Сериализатор подтверждения кода"""

    email = serializers.EmailField(max_length=50, required=True)
    code = serializers.CharField(max_length=4, required=True)
