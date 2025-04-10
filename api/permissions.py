from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 1)

class IsClientePremium(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 2)

class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 3)
