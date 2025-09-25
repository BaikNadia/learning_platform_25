from rest_framework import generics, filters, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, PublicUserSerializer, UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование профиля.
    - Любой авторизованный пользователь может просматривать.
    - Только владелец может редактировать.
    - При просмотре чужого профиля — только публичные поля.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем пользователя из URL: /api/users/5/
        user_id = self.kwargs.get('pk')
        return generics.get_object_or_404(User, id=user_id)

    def get_serializer_class(self):
        target_user = self.get_object()

        # Если смотрит владелец — полный сериализатор
        if target_user == self.request.user:
            return UserProfileSerializer

        # Если кто-то другой — только публичные данные
        return PublicUserSerializer

    def perform_update(self, serializer):
        # Запрещаем редактировать чужой профиль
        target_user = self.get_object()
        if target_user != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свой профиль.")
        serializer.save()


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'paid_course': ['exact'],
        'paid_lesson': ['exact'],
        'payment_method': ['exact'],
    }
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    Получение и редактирование профиля текущего пользователя
    URL: /api/users/me/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterUserAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    Доступен без авторизации.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]  # 👈 разрешено всем
