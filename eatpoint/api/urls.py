from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.users import (
    SignUp,
    ConfirmCodeView,
    UserViewSet,
    ConfirmCodeRefreshView,
    DjoserUserViewSet,
    MyTokenObtainPairView,
    MyTokenRefreshView,
)
from api.views.establishments import EstablishmentViewSet, ReviewViewSet

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register(
    r"establishments/(?P<establishment_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router.register("users", UserViewSet, basename="users"),

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/confirm-code/", ConfirmCodeView.as_view()),
    path("v1/auth/confirm-code-refresh/", ConfirmCodeRefreshView.as_view()),
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
    path(
        "v1/login/jwt/create/", MyTokenObtainPairView.as_view(), name="login"
    ),
    path(
        "v1/login/jwt/refresh/", MyTokenRefreshView.as_view(), name="refresh"
    ),
    # path("v1/login/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
