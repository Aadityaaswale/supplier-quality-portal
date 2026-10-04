from rest_framework import permissions


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None
    if hasattr(user, 'profile'):
        return user.profile.role
    return None


class IsAdminUserRole(permissions.BasePermission):
    """Enforces Admin role only."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser
            or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')
        )


class IsQualityManagerOrAdmin(permissions.BasePermission):
    """Enforces Quality Manager or Admin permissions."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'profile'):
            return request.user.profile.role in ['ADMIN', 'QUALITY_MANAGER']
        return False


class IsReviewerOrHigher(permissions.BasePermission):
    """Enforces Reviewer, Quality Manager, or Admin permissions."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
