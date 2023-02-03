from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin
from users.models import User
from users.serializers import (GetTokenSerializer,
                               SignUpSerializer, UserSerializer)
from users.utils import generate_and_send_code


@api_view(["POST"])
def user_signup(request):
    """Создание нового пользователя и отправка кода подтверждения в почту"""
    username = request.data.get("username")

    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid:
            return Response(
                'Username "me" запрещен', status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        generate_and_send_code(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data["email"] == user.email:
        serializer.save()
        generate_and_send_code(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        "Почта указана неверно!", status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def user_gettoken(request):
    """Проверка кода подтверждения и создание access-токена"""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            "Пользователь не найден", status=status.HTTP_404_NOT_FOUND
        )
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token_data = {"token": str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        "Неверный код подтверждения", status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(ModelViewSet):
    """Обработка учетных записей.
    Админам - всех.
    Авторизованным пользователям - только своих.
    """
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = 'username'
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=(['GET', 'PATCH']),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Получение и изменение своей учетной записи"""
        # Если это GET-запрос:
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        # Если это PATCH-запрос:
        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        # Если данные некорректны:
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError("Неверные данные")
        serializer.save(role=request.user.role)
        # Если данные корректны:
        return Response(serializer.data, status=status.HTTP_200_OK)
