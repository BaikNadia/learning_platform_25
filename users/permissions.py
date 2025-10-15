from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает:
    - Просмотр и редактирование — модераторам
    - Только просмотр — другим авторизованным пользователям
    - Ничего — неавторизованным
    """

    def has_permission(self, request, view):
        # Все авторизованные могут просматривать
        if not request.user.is_authenticated:
            return False

        # GET, HEAD, OPTIONS — разрешены всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True

        # POST, PUT, PATCH, DELETE — только если пользователь НЕ модератор
        is_moderator = request.user.groups.filter(name='moderators').exists()

        # ❌ Модераторы НЕ могут создавать или удалять
        if is_moderator and request.method in ['POST', 'DELETE']:
            return False

        # ✅ Модераторы могут редактировать (PUT, PATCH)
        if is_moderator and request.method in ['PUT', 'PATCH']:
            return True

        # Остальные (например, владельцы) могут всё
        return True
