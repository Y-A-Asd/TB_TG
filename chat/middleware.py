from jwt import decode, InvalidTokenError
from core.models import User
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
import os

SECRET_KEY = 'django-insecure-0uwk9*8mltebnrrdn(zawxdyh-8b*s6$!0n(lb(cwlk+@otvzq' #todo


@database_sync_to_async
def get_user(token):
    try:
        print('token', token)
        print('SECRET_KEY', SECRET_KEY)
        decoded_token = decode(token, SECRET_KEY, algorithms=['HS256'])
        print('decoded_token', decoded_token)
        user_id = decoded_token.get('user_id')
        print('get user id by jwt :::::::::', user_id)
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
                token = headers[b'authorization']
                scope['user'] = await get_user(token)
                print('done scopeee', scope['user'])
            except IndexError:
                print('Index Erroooooooooor')
                pass  # Malformed authorization header
        return await super().__call__(scope, receive, send)
