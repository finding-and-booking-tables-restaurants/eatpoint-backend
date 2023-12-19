from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v2.views.analytics import (
    AnalyticsHistoryListViewSet,
    AnalyticsHistoryViewSet,
    AnalyticsViewSet,
    AnalyticsListViewSet,
)
from api.v2.views.code_generate import (
    SendCodeForAnonymous,
    VerifyCodeForAnonymous,
)
from api.v2.views.establishments import (
    ZoneViewSet,
    CityViewSet,
    EstablishmentBusinessViewSet,
    FavoriteViewSet,
    ImageEstablishmentViewSet,
    EventUsersViewSet,
    EventBusinessViewSet,
)
from api.v2.views.reservation import (
    ReservationsEditViewSet,
    ReservationsUserListViewSet,
    ReservationsHistoryListViewSet,
    ReservationsRestorateurListViewSet,
    AvailableSlotsViewSet,
    # DateAvailabilityView,
    # TimeAvailabilityView,
)
from api.v2.views.reviews import OwnerResponseCreateView, ReviewViewSet
from api.v2.views.users import (
    SignUp,
    ConfirmCodeView,
    UserViewSet,
    ConfirmCodeRefreshView,
    DjoserUserViewSet,
    MyTokenObtainPairView,
    MyTokenRefreshView,
)
from api.v2.views.establishments import (
    EstablishmentViewSet,
    KitchenViewSet,
    ServicesViewSet,
    TypeEstViewSet,
)

app_name = "api"

router_v2 = DefaultRouter()

router_v2.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router_v2.register(
    r"establishments/(?P<establishment_id>\d+)/zones",
    ZoneViewSet,
    basename="zones",
)
router_v2.register(
    r"establishments/(?P<establishment_id>\d+)/reservations",
    ReservationsEditViewSet,
    basename="reservations",
)
router_v2.register(
    "reservations/history",
    ReservationsHistoryListViewSet,
    basename="reservationslisthistory",
)
router_v2.register(
    "reservations", ReservationsUserListViewSet, basename="reservationslist"
)
router_v2.register(
    "business/reservations",
    ReservationsRestorateurListViewSet,
    basename="reservations-business",
)
router_v2.register(
    "business/establishments",
    EstablishmentBusinessViewSet,
    basename="establishments-business",
)
router_v2.register("kitchens", KitchenViewSet, basename="Kitchens")
router_v2.register("services", ServicesViewSet, basename="service")
router_v2.register("types", TypeEstViewSet, basename="types")
router_v2.register("cities", CityViewSet, basename="cities")
router_v2.register(
    r"establishments/(?P<establishment_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router_v2.register("users", UserViewSet, basename="users"),
router_v2.register(
    r"establishments/(?P<establishment_id>\d+)/availability",
    AvailableSlotsViewSet,
    basename="availability",
)
router_v2.register(
    r"images/(?P<establishment_id>\d+)",
    ImageEstablishmentViewSet,
    basename="image",
)
router_v2.register(
    r"establishments/(?P<establishment_id>\d+)/events",
    EventUsersViewSet,
    basename="events",
),
router_v2.register(
    r"business/(?P<establishment_id>\d+)/events",
    EventBusinessViewSet,
    basename="events-business",
)

urlpatterns = [
    path("auth/signup/", SignUp.as_view()),
    path("auth/confirm-code/", ConfirmCodeView.as_view()),
    path("auth/confirm-code-refresh/", ConfirmCodeRefreshView.as_view()),
    path("auth/send-reservations-code/", SendCodeForAnonymous.as_view()),
    path("auth/verify-reservations-code/", VerifyCodeForAnonymous.as_view()),
    path(
        "reset-password/",
        DjoserUserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "reset-password-confirm/<str:uid>/<str:token>/",
        DjoserUserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset_password_confirm",
    ),
    path(
        "business/analytics/<int:establishment_id>/",
        AnalyticsViewSet.as_view(),
        name="establishment-analytics",
    ),
    path(
        "business/analytics/all/",
        AnalyticsListViewSet.as_view(),
        name="establishment-analytics-list",
    ),
    path(
        "business/analytics/history/<int:establishment_id>/",
        AnalyticsHistoryViewSet.as_view(),
        name="establishment-analytics-history",
    ),
    path(
        "business/analytics/history/all/",
        AnalyticsHistoryListViewSet.as_view(),
        name="establishment-analytics-list-history",
    ),
    # path(
    #     "availability/time/<str:dates>/<int:establishment_id>/",
    #     TimeAvailabilityView.as_view(),
    # ),
    # path(
    #     "availability/date/<int:zone_id>/", DateAvailabilityView.as_view()
    # ),
    path(
        "establishments/<int:establishment_id>/favorite/",
        FavoriteViewSet.as_view(),
    ),
    path("login/jwt/create/", MyTokenObtainPairView.as_view(), name="login"),
    path("login/jwt/refresh/", MyTokenRefreshView.as_view(), name="refresh"),
    path(
        "reviews/<int:review_id>/owner-response/",
        OwnerResponseCreateView.as_view(),
        name="create_owner_response",
    ),
    path("", include(router_v2.urls)),
]
