from rest_framework import permissions

import core.constants


class IsUserReservationCreate(permissions.BasePermission):
    """Возвращает результат проверки роли пользователя True если клиент."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == core.constants.CLIENT

        elif request.user.is_anonymous:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.user is not None:
            return obj.user == request.user


class IsClient(permissions.BasePermission):
    """Возвращает результат проверки роли пользователя True если клиент."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == core.constants.CLIENT

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsRestorateur(permissions.BasePermission):
    """
    Возвращает результат проверки роли пользователя True если ресторатор.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == core.constants.RESTORATEUR

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == core.constants.RESTORATEUR


class ReadOnly(permissions.BasePermission):
    """
    Возвращает результат проверки методов HTTP запросов
    True если 'GET', 'HEAD', 'OPTIONS'.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsOwnerRestaurant(permissions.BasePermission):
    """
    Возвращает True если пользователь является владельцем заведения.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAuthor(permissions.BasePermission):
    """
    Разрешение для редактирования если пользователь является автором объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user


class CreateRestaurant(permissions.BasePermission):
    """
    Разрешение для создания ресторана пользователь прошел аутентификацию и
    является ресторатором, либо только просмотр списка заведений.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "POST" and request.user.is_restorateur:
                return True
        return request.method in permissions.SAFE_METHODS


class IsAdministrator(permissions.BasePermission):
    """
    Возвращает True если пользователь является администратором.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_administrator
