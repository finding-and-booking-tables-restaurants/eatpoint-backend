from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.establishments import EstablishmentViewSet
from api.views.user import (
    SignUp,
    TokenView,
    UserViewSet,
)

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register("users", UserViewSet, basename="users"),

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/token/", TokenView.as_view()),
    path("v1/auth/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
