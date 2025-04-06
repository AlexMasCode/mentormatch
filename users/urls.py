# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    # Регистрация нового пользователя
    path('register/', RegisterView.as_view(), name='register'),
    # Аутентификация (логин) с выдачей JWT токенов
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # Обновление access-токена с использованием refresh-токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Выход из системы (аннулирование refresh-токена)
    path('logout/', LogoutView.as_view(), name='logout'),
    # Изменение пароля для аутентифицированного пользователя
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    # Инициирование сброса пароля (отправка ссылки на email)
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # Подтверждение сброса пароля (приём нового пароля по ссылке)
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
