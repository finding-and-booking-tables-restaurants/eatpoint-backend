from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.analytics import AnalyticsViewSet, AnalyticsListViewSet
from api.views.establishments import ZoneViewSet, CityViewSet
from api.views.reservation import (
    ReservationsViewSet,
    ReservationsListViewSet,
    ReservationsHistoryListViewSet,
)
from api.views.users import (
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
router.register(
    r"establishments/(?P<establishment_id>\d+)/zones",
    ZoneViewSet,
    basename="zones",
)
router.register(
    r"establishments/(?P<establishment_id>\d+)/reservations",
    ReservationsViewSet,
    basename="reservations",
)

router.register(
    "reservations/history",
    ReservationsHistoryListViewSet,
    basename="reservationslisthistory",
)
router.register(
    "reservations", ReservationsListViewSet, basename="reservationslist"
)
router.register("kitchens", KitchenViewSet, basename="Kitchens")
router.register("services", ServicesViewSet, basename="service")
router.register("types", TypeEstViewSet, basename="types")
router.register("cities", CityViewSet, basename="cities")
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
        "analytics/<int:establishment_id>/",
        AnalyticsViewSet.as_view(),
        name="establishment-analytics",
    ),
    path(
        "analytics/all/",
        AnalyticsListViewSet.as_view(),
        name="establishment-analytics-list",
    ),
    path(
        "v1/login/jwt/create/", MyTokenObtainPairView.as_view(), name="login"
    ),
    path(
        "v1/login/jwt/refresh/", MyTokenRefreshView.as_view(), name="refresh"
    ),
    path("v1/", include(router.urls)),
]
