from rest_framework import serializers
from .models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    Позволяет редактировать имя, телефон, город, аватар.
    Email и ID — только для чтения.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar')
        read_only_fields = ('id', 'email')  # email нельзя менять


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежей.
    Выводит все поля модели Payment.
    """
    class Meta:
        model = Payment
        fields = '__all__'
