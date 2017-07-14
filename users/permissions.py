from django.conf import settings

from rest_framework import permissions

from users.models import Patient, Doctor

RIKANG_KEY = 'powerformer'


class RikangKeyPermission(permissions.BasePermission):
    """Global permission check for unknown requests."""

    def has_permission(self, request, view):
        return True
        # uncomment this in production environment!
        # return request.META.get('HTTP_RIKANG_KEY') == RIKANG_KEY


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner.user == request.user


class IsPatient(permissions.BasePermission):
    """Permission check whether this request is from a patient."""

    def has_permission(self, request, view):
        return Patient.objects.filter(user=request.user).exists()


class IsDoctor(permissions.BasePermission):
    """Permission check whether this request is from a patient."""

    def has_permission(self, request, view):
        return Doctor.objects.filter(user=request.user).exists()
