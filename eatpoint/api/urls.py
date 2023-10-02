from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SignUp,
    TokenView,
    UserView,
)

router = DefaultRouter()

router.register("users", UserView),

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/token/", TokenView.as_view()),
    path("v1/", include(router.urls)),
]
