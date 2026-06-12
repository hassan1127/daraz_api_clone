from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Anyone can read, only admin can write."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsAdminOrSeller(BasePermission):
    """Admin and sellers can create. Anyone can read."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'SELLER']

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == 'ADMIN':
            return True
        # seller can only edit/delete their own objects
        return obj.seller == request.user


class IsAdmin(BasePermission):
    """Only admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
