from rest_framework import permissions

import core.constants


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == core.constants.CLIENT

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsRestorateur(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == core.constants.RESTORATEUR

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsOwnerRestaurant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user


class CreateRestaurant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "POST" and request.user.is_restorateur:
                return True
        return request.method in permissions.SAFE_METHODS
