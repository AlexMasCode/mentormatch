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
    # User registration
    path('register/', RegisterView.as_view(), name='register'),
    # Authentication (login) with JWT token issuance
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    # Refresh the access token using a refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Logout (invalidate the refresh token)
    path('logout/', LogoutView.as_view(), name='logout'),
    # Change password for an authenticated user
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    # Initiate password reset (send reset link via email)
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # Confirm password reset (accept new password via reset link)
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
