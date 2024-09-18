# order/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        self.room_name = "orders"
        self.room_group_name = "orders_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive WebSocket message from the client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']
        order_status = text_data_json['order_status']

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'order_status': order_status
            }
        )

    # Receive message from room group
    async def order_status_update(self, event):
        order_id = event['order_id']
        order_status = event['order_status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'order_id': order_id,
            'order_status': order_status
        }))

class HelloWorldConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        pass

    # Receive WebSocket message from the client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', 'Hello, World!')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))