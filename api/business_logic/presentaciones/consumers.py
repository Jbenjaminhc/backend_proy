import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.data_access.models.presentacion import Presentacion
from api.models import User

class CanvasSyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.presentacion_id = self.scope['url_route']['kwargs']['presentacion_id']
        self.group_name = f'presentacion_{self.presentacion_id}'

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        try:
            presentacion = await database_sync_to_async(Presentacion.objects.get)(pk=self.presentacion_id)
            is_owner = presentacion.creada_por_id == user.id
            is_collaborator = await database_sync_to_async(presentacion.colaboradores.filter(id=user.id).exists)()
            if not (is_owner or is_collaborator):
                await self.close()
                return
        except Presentacion.DoesNotExist:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_update',
                'message': text_data
            }
        )

    async def broadcast_update(self, event):
        await self.send(text_data=event['message'])