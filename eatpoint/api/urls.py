from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reservation.views import ReservationsViewSet
from api.views.establishments import EstablishmentViewSet
from api.views.user import (
    SignUp,
    TokenView,
    UserView,
)

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register("users", UserView),
router.register('reservations', ReservationsViewSet)

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/token/", TokenView.as_view()),
    path("v1/", include(router.urls)),
]
