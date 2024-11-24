import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.group_name = f"document_{self.document_id}"

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle messages received from the WebSocket
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "document_update",
                "message": data["message"],
            },
        )

    async def document_update(self, event):
        # Broadcast messages to the WebSocket
        await self.send(text_data=json.dumps(event))
