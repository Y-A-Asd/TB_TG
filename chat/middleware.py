from jwt import decode, InvalidTokenError
from core.models import User
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
import os


SECRET_KEY = os.getenv('SECRET_KEY')


@database_sync_to_async
def get_user(token):
    try:
        print('token', token)
        decoded_token = decode(str(token), str(SECRET_KEY), algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if user_id:
            return User.objects.get(pk=user_id)
        else:
            return None
    except (InvalidTokenError, User.DoesNotExist):
        return None


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token = headers[b'authorization'].decode().split()[1]
                scope['user'] = await get_user(token)
            except IndexError:
                pass  # Malformed authorization header
        return await super().__call__(scope, receive, send)