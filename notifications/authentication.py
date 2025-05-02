from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.authentication import get_authorization_header
from django.contrib.auth.models import AnonymousUser

class StatelessUser:
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True

    def __str__(self):
        return f"StatelessUser({self.id})"

class SimpleJWTWithoutDB(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if user_id is None:
            raise InvalidToken("Token missing user_id claim")
        return StatelessUser(user_id)
