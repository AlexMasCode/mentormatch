# auth_service/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Все эндпоинты аутентификации будут начинаться с /auth/
    path('auth/', include('users.urls')),
]
