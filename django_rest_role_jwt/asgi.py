import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import api.business_logic.presentaciones.routing as presentacion_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_role_jwt.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            presentacion_routing.websocket_urlpatterns
        )
    ),
})