from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Разрешения для категорий, жанров и произведений."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class ReviewAndCommentPermission(BasePermission):
    """Разрешения для отзывов и комментариев."""

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdmin(BasePermission):
    """Проверка, является ли пользователь админом."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
