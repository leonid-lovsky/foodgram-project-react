from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return False

    def has_object_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return False


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        return False
