from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.establishments import EstablishmentViewSet, ReviewViewSet
from api.views.users import UserViewSet, SignUp

router = DefaultRouter()

router.register(
    "establishments", EstablishmentViewSet, basename="establishments"
)
router.register(
    r"establishment/(?P<establishment_id>\d+)/reviews",
    ReviewViewSet,
    basename="review",
)
router.register("users", UserViewSet),

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/", include(router.urls)),
]
