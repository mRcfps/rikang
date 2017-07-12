from django.conf import settings

from rest_framework import permissions

RIKANG_KEY = 'powerformer'


class RikangKeyPermission(permissions.BasePermission):
    """Global permission check for unknown requests."""

    def has_permission(self, request, view):
        if settings.DEBUG:
            return True
        else:
            # production environment
            return request.META.get('HTTP_RIKANG_KEY') == RIKANG_KEY