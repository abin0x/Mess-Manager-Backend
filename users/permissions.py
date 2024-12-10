from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is trying to access or edit their own data.
        """
        # Allow GET, PUT, PATCH, DELETE only if the user is the owner of the object
        return obj == request.user


class IsManager(permissions.BasePermission):
    """
    Custom permission to allow only managers to perform specific actions.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the 'manager' role.
        """
        return request.user.is_authenticated and request.user.user_type == "manager"
