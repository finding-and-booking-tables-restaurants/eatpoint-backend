from django.conf import settings as django_settings
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.permissions import IsAnonymous
from api.serializers.code_generate import (
    SMSSendSerializer,
    SMSVerifySerializer,
)
from core.services import generate_reservation_code
from reservation.models import ConfirmationCode


@extend_schema(
    tags=["Подтверждение email (бронирование)"],
    methods=["POST"],
    description="Не авторизованный пользователь",
)
@extend_schema_view(
    post=extend_schema(
        summary="Отправить код",
        request=SMSSendSerializer(),
    ),
)
class SendCodeForAnonymous(GenericAPIView):
    """Отправка кода"""

    permission_classes = [IsAnonymous]
    serializer_class = SMSSendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            if ConfirmationCode.objects.filter(email=email).exists():
                ConfirmationCode.objects.filter(email=email).delete()
            code = generate_reservation_code()
            send_mail(
                "Код подтверждения",
                f"Ваш код подтверждения {code}",
                django_settings.EMAIL_HOST_USER,
                [email],
            )
            ConfirmationCode.objects.create(email=email, code=code)
            return Response(
                {"detail": f"Код подтверждения отправлен на {email}"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Подтверждение email (бронирование)"],
    methods=["POST"],
    description="Не авторизованный пользователь",
)
@extend_schema_view(
    post=extend_schema(
        summary="Подтвердить код",
        request=SMSVerifySerializer(),
    ),
)
class VerifyCodeForAnonymous(GenericAPIView):
    """Подтверждение кода"""

    permission_classes = [IsAnonymous]
    serializer_class = SMSVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        try:
            confirmation_code = ConfirmationCode.objects.get(
                email=email,
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
            {"detail": "email подтвержден!"},
            status=status.HTTP_200_OK,
        )
