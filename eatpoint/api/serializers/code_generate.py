from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class SMSSendSerializer(serializers.Serializer):
    """Сериализатор отправки кода"""

    telephone = PhoneNumberField(required=True)


class SMSVerifySerializer(serializers.Serializer):
    """Сериализатор подтверждения код"""

    telephone = PhoneNumberField(required=True)
    code = serializers.CharField(max_length=4, required=True)
