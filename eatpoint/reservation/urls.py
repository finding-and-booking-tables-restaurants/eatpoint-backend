from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import ReservationsViewSet

# Создаётся роутер
router = SimpleRouter()
# Вызываем метод .register с нужными параметрами
router.register('reservations', ReservationsViewSet)
# В роутере можно зарегистрировать любое количество пар "URL, viewset":
# например


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('', include(router.urls)),
] 