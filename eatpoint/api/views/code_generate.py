import asyncio

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAnonymous
from api.serializers.code_generate import (
    SMSSendSerializer,
    SMSVerifySerializer,
)
from core.services import generate_reservation_code
from core.tgbot import send_code
from reservation.models import ConfirmationCode


@extend_schema(
    tags=["Подтверждение номер телефона(бронирование)"],
    methods=["POST"],
    description="Не авторизованный пользователь",
)
@extend_schema_view(
    post=extend_schema(
        summary="Отправить код",
        request=SMSSendSerializer(),
    ),
)
class SendSMSCode(APIView):
    """Отправка кода"""

    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = SMSSendSerializer(data=request.data)
        if serializer.is_valid():
            telephone = serializer.validated_data["telephone"]
            if ConfirmationCode.objects.filter(
                phone_number=telephone
            ).exists():
                ConfirmationCode.objects.filter(
                    phone_number=telephone
                ).delete()
            code = generate_reservation_code()
            asyncio.run(send_code(f"Ваш код подтверждения {code}"))
            ConfirmationCode.objects.create(phone_number=telephone, code=code)
            return Response(
                {
                    "detail": f"Смс с кодом подтверждения отправлено на номер {telephone}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Подтверждение номер телефона(бронирование)"],
    methods=["POST"],
    description="Не авторизованный пользователь",
)
@extend_schema_view(
    post=extend_schema(
        summary="Подтвердить номер",
        request=SMSVerifySerializer(),
    ),
)
class VerifySMSCode(APIView):
    """Подтверждение кода"""

    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = SMSVerifySerializer(data=request.data)
        if serializer.is_valid():
            telephone = serializer.validated_data["telephone"]
            code = serializer.validated_data["code"]
            try:
                confirmation_code = ConfirmationCode.objects.get(
                    phone_number=telephone,
                    code=code,
                    is_verified=False,
                )
            except ConfirmationCode.DoesNotExist:
                return Response(
                    {"detail": "Неверный код подтверждения"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            confirmation_code.is_verified = True
            confirmation_code.save()
            return Response(
                {"detail": "Номер телефона подтвержден!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
