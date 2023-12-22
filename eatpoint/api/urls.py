from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.analytics import (
    AnalyticsHistoryListViewSet,
    AnalyticsHistoryViewSet,
    AnalyticsViewSet,
    AnalyticsListViewSet,
)
from api.views.code_generate import SendSMSCode, VerifySMSCode
from api.views.events import (
    TypeEventViewset,
    EventBusinessViewSet,
    EventPhotoViewset,
    EventUsersViewSet,
)
from api.views.establishments import (
    ZoneViewSet,
    CityViewSet,
    EstablishmentBusinessViewSet,
    FavoriteViewSet,
    ImageEstablishmentViewSet,
)
from api.views.reservation import (
    ReservationsEditViewSet,
    ReservationsUserListViewSet,
    ReservationsHistoryListViewSet,
    ReservationsRestorateurListViewSet,
    AvailabilityViewSet,
    DateAvailabilityView,
    TimeAvailabilityView,
)
from api.views.reviews import OwnerResponseCreateView, ReviewViewSet
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
    KitchenViewSet,
    ServicesViewSet,
    TypeEstViewSet,
)

app_name = "api"

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
    ReservationsEditViewSet,
    basename="reservations",
)
router.register(
    "reservations/history",
    ReservationsHistoryListViewSet,
    basename="reservationslisthistory",
)
router.register(
    "reservations", ReservationsUserListViewSet, basename="reservationslist"
)
router.register(
    "business/reservations",
    ReservationsRestorateurListViewSet,
    basename="reservations-business",
)
router.register(
    "business/establishments",
    EstablishmentBusinessViewSet,
    basename="establishments-business",
)
router.register("kitchens", KitchenViewSet, basename="Kitchens")
router.register("services", ServicesViewSet, basename="service")
router.register("types", TypeEstViewSet, basename="types")
router.register("cities", CityViewSet, basename="cities")
router.register("event_types", TypeEventViewset, basename="event-types")
router.register(
    r"establishments/(?P<establishment_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router.register("users", UserViewSet, basename="users"),
router.register(
    r"establishments/(?P<establishment_id>\d+)/availability",
    AvailabilityViewSet,
    basename="availability",
)
router.register(
    r"images/(?P<establishment_id>\d+)",
    ImageEstablishmentViewSet,
    basename="image",
)
router.register(
    r"establishments/(?P<establishment_id>\d+)/events",
    EventUsersViewSet,
    basename="events",
),
router.register(
    r"business/(?P<establishment_id>\d+)/events",
    EventBusinessViewSet,
    basename="events-business",
)
router.register(
    r"business/(?P<establishment_id>\d+)/events/(?P<event_id>\d+)/photos",
    EventPhotoViewset,
    basename="events-photos",
)

urlpatterns = [
    path("auth/signup/", SignUp.as_view()),
    path("auth/confirm-code/", ConfirmCodeView.as_view()),
    path("auth/confirm-code-refresh/", ConfirmCodeRefreshView.as_view()),
    path("auth/send-reservations-code/", SendSMSCode.as_view()),
    path("auth/verify-reservations-code/", VerifySMSCode.as_view()),
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
    path(
        "availability/time/<str:dates>/<int:establishment_id>/",
        TimeAvailabilityView.as_view(),
    ),
    path("availability/date/<int:zone_id>/", DateAvailabilityView.as_view()),
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
    path("", include(router.urls)),
]
