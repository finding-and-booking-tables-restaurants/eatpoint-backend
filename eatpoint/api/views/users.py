from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from djoser import views

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from api.permissions import IsUser, IsRestaurateur
from api.serializers.users import (
    MeSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    CodeSerializer,
)


@extend_schema(tags=["Пользователи"], methods=["GET", "PATCH"])
@extend_schema_view(
    list=extend_schema(
        summary="Список пользователей",
    ),
    # me=extend_schema(
    #     summary="Детальная информация о текущем пользователе",
    # ),
    retrieve=extend_schema(
        summary="Детальная информация о пользователе (id=номер телефона)",
    ),
    # destroy=extend_schema(
    #     summary="Детальная информация о пользователе (id=номер телефона)",
    # ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    lookup_field = "telephone"
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Редактирование профиля",
        methods=["PATCH"],
    )
    @extend_schema(
        summary="Профиль пользователя",
        methods=["GET"],
    )
    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsUser | IsRestaurateur, IsAuthenticated),
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


@extend_schema(tags=["SignUp"], methods=["POST"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация",
    ),
)
class SignUp(APIView):
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
                is_agreement=False,
            )
            user.set_password(request.data.get("password"))
            message = user.confirm_code
            user.confirmation_code = message
            user.save()
            send_mail(
                "Код подтверждения EatPoint",
                f"Код для подтверждения на сайте: {message}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            if created:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                "На Ваш email отправлен код подтверждения",
                status=status.HTTP_200_OK,
            )
        except IntegrityError:
            return Response(
                "Аккаунт уже зарегистрирован, авторизуйтесь...",
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(tags=["SignUp"], methods=["POST"])
@extend_schema_view(
    post=extend_schema(
        summary="Получить код подтверждения",
    ),
)
class TokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telephone = request.data.get("telephone")
        confirmation_code = request.data.get("confirmation_code")
        is_agreement = request.data.get("is_agreement")
        if not is_agreement:
            return Response(
                "Необходимо согласиться с Условиями пользования.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not User.objects.filter(telephone=telephone).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(telephone=telephone)
        if user.is_active:
            return Response(
                "Аккаунт уже зарегистрирован, авторизуйтесь",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.confirmation_code == confirmation_code:
            user.is_active = True
            user.is_agreement = True
            user.confirmation_code = ""
            user.save()

            send_mail(
                "Аккаунт зарегистрирован",
                "Для перехода в профиль нажмите на ссылку: ...",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(
                # {"token": user.token},
                "Аккаунт зарегистрирован",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            "Вы ввели не правильный код",
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(tags=["SignUp"], methods=["POST"])
@extend_schema_view(
    post=extend_schema(
        summary="Обновление кода подтверждения",
    ),
)
class ConfirmCodeRefresh(APIView):
    serializer_class = CodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telephone = request.data.get("telephone")

        if not User.objects.filter(telephone=telephone).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(telephone=telephone)
        user.confirmation_code = user.confirm_code
        message = user.confirmation_code
        user.save()

        send_mail(
            "Код подтверждения EatPoint",
            f"Код для подтверждения на сайте: {message}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=["Password"], methods=["POST"])
@extend_schema_view(
    reset_password=extend_schema(
        summary="Сброс пароля",
    ),
    reset_password_confirm=extend_schema(
        summary="Подтверждение сброса пароля",
    ),
)
class DjoserUserViewSet(views.UserViewSet):
    pass
