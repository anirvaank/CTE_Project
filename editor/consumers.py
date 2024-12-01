from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.room_group_name = f'editor_{self.document_id}'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)

        data = json.loads(text_data)
        message = data['message']

        # Send message to the WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'editor_message',
                'message': message,
            }
        )

    async def editor_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
