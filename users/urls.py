from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView, CustomTokenObtainPairView,
)

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    # Refresh the access token using a refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('password/change/', PasswordChangeView.as_view(), name='password_change'),

    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),

    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
