# portal/utils/jwt.py
import jwt, base64, json
from django.conf import settings

def peek_jwt(access: str) -> dict:
    """
    Раскодировать **payload** JWT *без проверки сигнатуры*  нужно
    только быстро узнать роль/имя, а не аутентифицировать пользователя.
    """
    try:
        # второй сегмент (payload) → base64url‑decode → json
        payload_b64 = access.split('.')[1] + '==='        # выровнять padding
        payload_json = base64.urlsafe_b64decode(payload_b64).decode()
        return json.loads(payload_json)
    except Exception:
        return {}


def decode_jwt_payload(token):
    try:
        payload_part = token.split('.')[1]
        # Добавляем padding если нужно
        padded = payload_part + '=' * (-len(payload_part) % 4)
        decoded = base64.urlsafe_b64decode(padded)
        return json.loads(decoded)
    except Exception as e:
        print("JWT decode error:", e)
        return {}
