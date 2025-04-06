# users/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

User = get_user_model()

# Регистрация нового пользователя
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# Логаут: добавление refresh-токена в blacklist
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

# Изменение пароля для аутентифицированного пользователя
class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

# Инициирование сброса пароля (здесь – просто демонстрация, реальная реализация требует отправки email)
class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            # Здесь необходимо сгенерировать токен и отправить email с ссылкой для сброса пароля
            # Для демонстрации вернём успешный ответ
            return Response({"detail": "Password reset link sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

# Подтверждение сброса пароля (приём нового пароля по ссылке из email)
class PasswordResetConfirmView(APIView):
    def post(self, request):
        # В реальной реализации сюда придёт uid и token, подтверждающие право сброса пароля
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        # Здесь необходимо проверить uid и token.
        # Для демонстрации примем, что проверка прошла успешно.
        try:
            user = User.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
