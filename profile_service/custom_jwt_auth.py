from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Instead of looking for the user in the local database, return a TokenUser
        generated from the token payload, and set is_staff based on the token payload.
        """
        # Attempt to retrieve the user ID from the "user_id" or "sub" field
        user_id = validated_token.get("user_id") or validated_token.get("sub")
        if user_id is None:
            raise InvalidToken("Token contained no recognizable user identification")
        user = TokenUser(validated_token)
        user.is_staff = validated_token.get("is_staff", False)
        return user
