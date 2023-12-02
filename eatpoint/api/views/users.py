import asyncio

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from djoser import views

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import filters, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import core.choices
import core.constants
from core.pagination import LargeResultsSetPagination
from core.tgbot import send_code
from users.models import User
from api.permissions import IsClient, IsRestorateur
from api.serializers.users import (
    MeSerializer,
    SignUpSerializer,
    ConfirmCodeSerializer,
    UserSerializer,
    ConfirmCodeRefreshSerializer,
)


@extend_schema(tags=["Users"], description="Администратор")
@extend_schema_view(
    list=extend_schema(summary="Список пользователей", methods=["GET"]),
    retrieve=extend_schema(
        summary="Детальная информация о пользователе (id=номер телефона)",
        methods=["GET"],
    ),
)
class UserViewSet(
    mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """
    Сет для отображения и редактирования профиля пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    pagination_class = LargeResultsSetPagination
    lookup_field = "telephone"
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Редактирование профиля",
        methods=["PATCH"],
        description="Клиент/ресторатор",
    )
    @extend_schema(
        summary="Профиль пользователя",
        methods=["GET"],
        description="Клиент/ресторатор",
    )
    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(
            IsClient | IsRestorateur | IsAdminUser,
            IsAuthenticated,
        ),
    )
    def me(self, request):
        serializer_class = MeSerializer
        if request.method == "GET":
            serializer = serializer_class(request.user, many=False)
            return Response(serializer.data)

        if request.method == "PATCH":
            user = User.objects.get(telephone=request.user.telephone)
            serializer = serializer_class(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["SignUp"], methods=["POST"], description="Незарегистрированный"
)
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация аккаунта",
    ),
)
class SignUp(APIView):
    """
    Сет для регистрации пользователя.
    """

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                telephone=request.data.get("telephone"),
                email=request.data.get("email"),
                role=request.data.get("role"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                is_active=False,
                is_agreement=request.data.get("is_agreement"),
                confirm_code_send_method=request.data.get(
                    "confirm_code_send_method"
                ),
            )
            message = ""
            if not created and user.is_active:
                return Response(
                    "Аккаунт уже подтвержден, авторизуйтесь...",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not created and not user.is_active:
                return Response(
                    "Аккаунт не активен, введите код подтверждения...",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if created:
                user.set_password(request.data.get("password"))
                msg_code = user.confirm_code
                user.confirmation_code = msg_code
                user.save()

                match user.confirm_code_send_method:
                    case core.constants.EMAIL:
                        send_mail(
                            "Код подтверждения EatPoint",
                            f"Код для подтверждения на сайте: {msg_code}",
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                        message = "На Ваш email отправлен код подтверждения"
                    case core.constants.SMS:
                        message = """
                            На Ваш телефон отправлена СМС с кодом подтверждения
                        """
                    case core.constants.TELEGRAM:
                        asyncio.run(
                            send_code(
                                f"Код для пользователя: {user.telephone} --> {msg_code}"
                            )
                        )
                        message = "В Телеграм отправлен код подтверждения"
                    case core.constants.NOTHING:
                        user.is_active = True
                        user.confirmation_code = ""
                        user.save()
                        message = "Аккаунт зарегистрирован, авторизуйтесь..."
                return Response(
                    serializer.data | {"message": message},
                    status=status.HTTP_201_CREATED,
                )
        except IntegrityError:
            return Response(
                "Проверьте вводимые данные и попробуйте ещё раз",
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["SignUp"], methods=["POST"], description="Зарегистрированный"
)
@extend_schema_view(
    post=extend_schema(
        summary="Подтвердить регистрацию",
    ),
)
class ConfirmCodeView(APIView):
    """
    Представление для подтверждения регистрации пользователя.
    """

    serializer_class = ConfirmCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telephone = request.data.get("telephone")
        confirmation_code = request.data.get("confirmation_code")

        if not User.objects.filter(telephone=telephone).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(telephone=telephone)

        if str(user.is_agreement).lower() not in ("true", "1", 1, True):
            return Response(
                "Необходимо согласиться с Условиями пользования.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.is_active:
            return Response(
                "Аккаунт уже зарегистрирован, войдите в систему",
                status=status.HTTP_400_BAD_REQUEST,
            )

        match user.confirm_code_send_method:
            case core.constants.NOTHING:
                user.is_active = True
                user.is_agreement = True
                user.confirmation_code = ""
                user.save()
                return Response(
                    "Аккаунт зарегистрирован, можете войти в систему",
                    status=status.HTTP_201_CREATED,
                )
            case core.constants.EMAIL:
                if user.confirmation_code == confirmation_code:
                    user.is_active = True
                    user.is_agreement = True
                    user.confirmation_code = ""
                    user.save()

                    send_mail(
                        "Аккаунт зарегистрирован",
                        "Для перехода в профиль перейдите по ссылке: https://eatpoint.site/signin",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    return Response(
                        "Аккаунт зарегистрирован, можете войти в систему",
                        status=status.HTTP_201_CREATED,
                    )
                return Response(
                    "Вы ввели не правильный код",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            case core.constants.SMS:
                pass
            case core.constants.TELEGRAM:
                if user.confirmation_code == confirmation_code:
                    user.is_active = True
                    user.is_agreement = True
                    user.confirmation_code = ""
                    user.save()

                    asyncio.run(
                        send_code(
                            f"Аккаунт для пользователя: {user.telephone} активирован"
                        )
                    )
                    return Response(
                        "Аккаунт зарегистрирован, можете войти в систему",
                        status=status.HTTP_201_CREATED,
                    )
                return Response(
                    "Вы ввели не правильный код",
                    status=status.HTTP_400_BAD_REQUEST,
                )


@extend_schema(
    tags=["SignUp"], methods=["POST"], description="Зарегистрированный"
)
@extend_schema_view(
    post=extend_schema(
        summary="Получить кода подтверждения повторно",
    ),
)
class ConfirmCodeRefreshView(APIView):
    """
    Представление повторной отправки кода подтверждения
    если пользователь его еще не ввел.
    """

    serializer_class = ConfirmCodeRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telephone = request.data.get("telephone")

        if not User.objects.filter(telephone=telephone).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(telephone=telephone)
        if user.is_active:
            return Response(
                "Аккаунт уже активирован, можете войти в систему",
                status=status.HTTP_200_OK,
            )
        user.confirmation_code = user.confirm_code
        message = user.confirmation_code
        user.save()

        match user.confirm_code_send_method:
            case core.constants.EMAIL:
                send_mail(
                    "Код подтверждения EatPoint",
                    f"Код для подтверждения на сайте: {message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return Response(
                    "Код подтверждения отправлен на email",
                    status=status.HTTP_200_OK,
                )

            case core.constants.TELEGRAM:
                asyncio.run(
                    send_code(
                        f"Код для пользователя: {user.telephone} --> {message}"
                    )
                )
                return Response(
                    "Код подтверждения отправлен в Telegram",
                    status=status.HTTP_200_OK,
                )

            case core.constants.SMS:
                pass


@extend_schema(
    tags=["Password"], methods=["POST"], description="Авторизованный"
)
@extend_schema_view(
    reset_password=extend_schema(
        summary="Сброс пароля",
    ),
    reset_password_confirm=extend_schema(
        summary="Подтверждение сброса пароля",
    ),
)
class DjoserUserViewSet(views.UserViewSet):
    """
    Сет для сброса и подтверждения сброса пароля пользователя.
    """


@extend_schema(tags=["Login"], description="Зарегистрированный")
@extend_schema_view(
    post=extend_schema(
        summary="Логин",
    ),
)
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Представление для входа пользователя в систему.
    """


@extend_schema(tags=["Login"], description="Зарегистрированный")
@extend_schema_view(
    post=extend_schema(
        summary="Обновление JWT токена",
    ),
)
class MyTokenRefreshView(TokenRefreshView):
    """
    Представление для обновления JWT.
    """
