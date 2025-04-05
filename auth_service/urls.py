# auth_service/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ендпоїнти реєстрації
    path('users/register/', RegisterView.as_view(), name='register'),
    # Ендпоїнти логіну та оновлення токенів
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
