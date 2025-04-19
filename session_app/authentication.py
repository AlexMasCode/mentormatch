# session_app/authentication.py
from types import SimpleNamespace
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWT
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class JWTAuthentication(BaseJWT):
    def get_user(self, validated_token):
        """
        Instead of searching the DB, we construct a simple user
        object with fields from the payload, and mark it as authenticated.
        """
        user_id = validated_token.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Token contained no recognizable user identification", code="user_not_found")
        role = validated_token.get("role")
        first_name = validated_token.get("first_name", "")
        last_name = validated_token.get("last_name", "")

        user = SimpleNamespace(
            id=user_id,
            role=role,
            first_name=first_name,
            last_name=last_name,
            is_authenticated=True,
        )
        return user
