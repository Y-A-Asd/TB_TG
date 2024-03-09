"""
ASGI config for TB_TG project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import django
import os
from chat import middleware, routing
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TB_TG.settings.dev')
django_asgi_app = get_asgi_application()
"""
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        middleware.JWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
})
"""

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        URLRouter(routing.websocket_urlpatterns))
})
