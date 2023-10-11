from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.establishments import EstablishmentViewSet
from api.views.user import (
    SignUp,
    ConfirmCodeView,
    UserViewSet,
    ConfirmCodeRefreshView,
    DjoserUserViewSet,
    MyTokenObtainPairView,
    MyTokenRefreshView,
)
from api.views.establishments import (
    EstablishmentViewSet,
    ReviewViewSet,
    KitchenViewSet,
    ServicesViewSet,
    TypeEstViewSet,
)

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register("users", UserView),

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
    path("v1/", include(router.urls)),
]
