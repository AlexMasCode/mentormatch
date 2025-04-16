from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.conf import settings
import requests

from .kafka_producer import publish_new_user_event
from .models import CustomUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

# Obtain JWT token pair (access and refresh) using custom serializer
@extend_schema(
    summary="Obtain JWT Token Pair",
    description="Obtain a JWT token pair by providing valid user credentials. Returns access and refresh tokens.",
    request=CustomTokenObtainPairSerializer,
    responses={
        200: CustomTokenObtainPairSerializer,
        400: OpenApiResponse(description="Bad Request - Invalid credentials")
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Register a new user
@extend_schema(
    summary="Register New User",
    description="Register a new user by providing the required fields. Returns the created user data on success.",
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
        400: OpenApiResponse(description="Bad Request - Invalid data")
    },
)
class RegisterView(APIView):
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "MENTEE")

        if role == "MENTOR":
            company_id = request.data.get("company_id")
            access_key = request.data.get("access_key")
            if not company_id or not access_key:
                return Response({"detail": "For mentors, company_id and access_key are required."},
                                status=status.HTTP_400_BAD_REQUEST)
            # Call Profile Service to check the access key
            profile_url = settings.PROFILE_SERVICE_URL  # "http://profile-service:8000/api/companies/validate-access/"
            payload = {"company_id": company_id, "access_key": access_key}
            try:
                resp = requests.post(profile_url, json=payload, timeout=5)
                if resp.status_code != 200 or not resp.json().get("valid"):
                    return Response({"detail": "Invalid company access key."}, status=status.HTTP_400_BAD_REQUEST)
            except requests.RequestException:
                return Response({"detail": "Unable to validate company access key."},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # If all checks have passed, we proceed to creating the user
        try:
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=role
            )
        except Exception as e:
            return Response({"detail": f"Error during registration: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if role == "MENTOR":
            publish_new_user_event(user, company_id)
        else:
            publish_new_user_event(user)

        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)


# Logout: Blacklist the refresh token to log out the user
@extend_schema(
    summary="Logout User",
    description="Logout an authenticated user by blacklisting their refresh token. Expects a 'refresh' token in the request body.",
    request={
        "type": "object",
        "properties": {
            "refresh": {"type": "string", "example": "your_refresh_token"}
        },
        "required": ["refresh"]
    },
    responses={
        205: OpenApiResponse(description="Logout successful."),
        400: OpenApiResponse(description="Bad Request - Invalid token")
    },
)
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


# Change password for the authenticated user
@extend_schema(
    summary="Change Password",
    description=(
        "Change the password for the currently authenticated user by providing the old password and "
        "the new password in the request body."
    ),
    request={
        "type": "object",
        "properties": {
            "old_password": {"type": "string", "example": "oldpassword123"},
            "new_password": {"type": "string", "example": "newpassword456"}
        },
        "required": ["old_password", "new_password"]
    },
    responses={
        200: OpenApiResponse(description="Password changed successfully."),
        400: OpenApiResponse(description="Bad Request - Incorrect old password or invalid data.")
    },
)
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


# Initiate password reset (for demonstration only)
@extend_schema(
    summary="Initiate Password Reset",
    description=(
        "Initiate a password reset process for the given email address. In a real implementation, "
        "a password reset link would be sent to the user's email address."
    ),
    request={
        "type": "object",
        "properties": {
            "email": {"type": "string", "example": "user@example.com"}
        },
        "required": ["email"]
    },
    responses={
        200: OpenApiResponse(description="Password reset link sent to email."),
        400: OpenApiResponse(description="Bad Request - User with this email does not exist.")
    },
)
class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            # In a real implementation, generate a token and send an email with the password reset link.
            return Response({"detail": "Password reset link sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)


# Confirm password reset by setting a new password (for demonstration only)
@extend_schema(
    summary="Confirm Password Reset",
    description=(
        "Confirm a password reset request. In a real implementation, both a valid UID and token are "
        "required to verify the password reset request."
    ),
    request={
        "type": "object",
        "properties": {
            "uid": {"type": "string", "example": "1"},
            "token": {"type": "string", "example": "reset-token"},
            "new_password": {"type": "string", "example": "newpassword456"}
        },
        "required": ["uid", "token", "new_password"]
    },
    responses={
        200: OpenApiResponse(description="Password reset successfully."),
        400: OpenApiResponse(description="Bad Request - Invalid user or token.")
    },
)
class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        try:
            user = User.objects.get(pk=uid)
            # In a real implementation, token and uid verification would take place here.
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
