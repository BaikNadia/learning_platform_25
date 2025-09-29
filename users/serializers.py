from rest_framework import serializers
from .models import User, Payment


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра чужого профиля.
    Только безопасная информация.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'city', 'avatar')


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'password')
        read_only_fields = ('id',)


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежей.
    Выводит все поля модели Payment.
    """
    class Meta:
        model = Payment
        fields = '__all__'
