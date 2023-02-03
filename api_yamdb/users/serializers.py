from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""

    def validate_username(self, value):
        """Проверяем, что username не является me"""
        if value.lower() == "me":
            raise serializers.ValidationError('username не может быть "me"')
        return value

    class Meta:
        model = User
        fields = ("email", "username")


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена"""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
