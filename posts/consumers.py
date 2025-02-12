import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

user_channel_map = {}

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_id = self.scope["user"].id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        user_channel_map[self.user_id] = self.channel_name
        self.accept()

        self.chat_message({"message":{
            'message': 'Connected',
            'from_user_id': self.user_id
        }})


    def disconnect(self, code):
        if self.user_id in user_channel_map:
            del user_channel_map[self.user_id]

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        target_user_id = text_data_json.get("target_user_id", None)

        if target_user_id:
            self.notify_user(target_user_id, message)
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))

    def notify_user(self, target_user_id, message):
        target_channel_name = user_channel_map.get(target_user_id)
        
        if target_channel_name:
            async_to_sync(self.channel_layer.send)(
                target_channel_name,
                {
                    "type": "chat.message",
                    "message": {
                        "message": message,
                        "from_user_id": self.user_id,
                    },
                }
            )