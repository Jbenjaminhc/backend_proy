from django.urls import path
from .consumers import CanvasSyncConsumer

websocket_urlpatterns = [
    path('ws/presentacion/<str:presentacion_id>/', CanvasSyncConsumer.as_asgi()),
]