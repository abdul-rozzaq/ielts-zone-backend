from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not isinstance(request.user, AnonymousUser))

