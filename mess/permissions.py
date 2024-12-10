from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Allows access only to users with user_type 'manager'
    """

    def has_permission(self, request, view):
        # Check if user is authenticated and is a manager
        return bool(request.user and request.user.is_authenticated and request.user.is_manager())


from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Allows access only to mess managers.
    """

    def has_permission(self, request, view):
        # Ensures that only authenticated managers can make this request
        return request.user.is_authenticated and hasattr(request.user, 'managed_messes') and request.user.managed_messes.exists()



class IsAuthenticatedAndUser(permissions.BasePermission):
    """
    Allows only authenticated users to send membership requests.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user.is_authenticated


