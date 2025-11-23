"""
ASGI config for sistema_veterinnaria project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notificaciones.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_veterinaria.settings")

django_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(notificaciones.routing.websocket_urlpatterns)
    ),
})
