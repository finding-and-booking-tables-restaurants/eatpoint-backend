from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.establishments import EstablishmentViewSet
from api.views.users import (
    SignUp,
    TokenView,
    UserViewSet,
    ConfirmCodeRefresh,
    DjoserUserViewSet,
)

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register("users", UserViewSet, basename="users"),

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/confirm-code/", TokenView.as_view()),
    path("v1/auth/confirm-code/refresh/", ConfirmCodeRefresh.as_view()),
    path(
        "v1/reset-password/",
        DjoserUserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "v1/reset-password-confirm/<str:uid>/<str:token>/",
        DjoserUserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset_password_confirm",
    ),
    # path("v1/login/", include('djoser.urls')),
    path("v1/login/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
