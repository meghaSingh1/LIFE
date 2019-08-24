# from channels.generic.websocket import WebsocketConsumer

# from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def init_chat(self, data):
#         profile_name = data['profile_name']
#         user = MyUser.objects.filter(profile_name=profile_name)
#         content = {
#             'command': 'init_chat'
#         }
#         if len(user) == 0:
#             content['error'] = 'User not exists'
#             self.send_message(content)
#         content['success'] = 'Chatting in with success with profile name: ' + profile_name
#         self.send_message(content)

#     def fetch_messages(self, data):
#         chat_room_id = data['chat_room_id']
#         chat_room = ChatRoom.objects.filter(pk=chat_room_id)
#         content = {
#             'command': 'chat_message'
#         }
#         if len(chat_room) == 0:
#             content['error'] = 'Chat room not exists'
#             self.send_message(content)

#         messages = Message.objects.filter(chat_room = chat_room[0])
#         content = {
#             'command': 'messages',
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)

#     def new_message(self, data):
#         profile_name = data['profile_name']
#         content = data['content']
#         chat_room_id = data['chat_room']
#         user = MyUser.objects.filter(profile_name=profile_name)
#         chat_room = ChatRoom.objects.filter(pk=chat_room_id)

#         message = Message.objects.create(user=user[0], content=content, chat_room=chat_room[0])
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         self.send_chat_message(content)

#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     def message_to_json(self, message):
#         return {
#             'user': message.user.first_name + message.user.last_name,
#             'content': message.content,
#             'date_created': str(message.date_created)
#         }

#     commands = {
#         'init_chat': init_chat,
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }

#     def connect(self):
#         self.user = self.scope['user']
#         self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
#         self.room_name = 'room-' + self.room_uuid
#         self.room_group_name = 'chat_%s' % self.room_name

#         self.room = ChatRoom.objects.filter(uuid=self.room_uuid)

#         if len(self.room) > 0:
#             if user in self.room[0].users.all():
#             # Join room group
#                 async_to_sync(self.channel_layer.group_add)(
#                     self.room_group_name,
#                     self.channel_name
#                 )
#                 self.accept()
#             else:
#                 self.close()
#         else:
#             self.close()


#     def disconnect(self, close_code):
#         # leave group room
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)

#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))

#     def send_chat_message(self, message):
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#         # Send message to WebSocket
#         self.send(text_data=json.dumps(message))

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from .models import MyUser, Message, ChatRoom
from rest_framework_simplejwt.tokens import AccessToken
import requests_async as requests
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from .serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join websocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.channel_name)
        await self.accept()
        
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': {
        #     'command': 'new_message',
        #     'message': 'Up'
        #     }
        # })
        

        # Send message to room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    # Fetch message for room group
    async def fetch_messages(self, event):
        messages = event['messages']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'fetch_messages',
            'message': messages
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_chat_room(self, room_uuid):
        return ChatRoom.objects.filter(uuid=room_uuid)

    @database_sync_to_async
    def get_user(self, user_profile_name):
        return MyUser.objects.filter(profile_name=user_profile_name)

    @database_sync_to_async
    def get_messages(self, room):
        return Message.objects.filter(chat_room = room)

    @database_sync_to_async
    def save_message(self, user, content, room):
        message = Message.objects.create(user = user, chat_room = room, content = content)
        return message

    # Send bulk messages
    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # Send message json
    async def message_to_json(self, message):
        return {
            'user': message.user.first_name + message.user.last_name,
            'content': message.content,
            'date_created': str(message.date_created)
        }

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        email = data['email']
        message = data['message']
        token = data['token']


        url = "http://127.0.0.1:8000/api/check_logged_in"

        payload = {"email": email, 'for_channels': 'channels'}

        header = {"Content-type": "application/json",
                'Authorization': "Bearer " + token}


        response = await requests.post(url, data=json.dumps(payload), headers=header)
        # data = json.loads(response.decode('utf-8'))
        response_json = response.json()
        print(response_json)
        if response_json['message'] == 'Authorized':
            room = await self.get_chat_room(self.room_name)
            user = await self.get_user(response_json['user']['profile_name'])
            if len(room) > 0 and len(user) > 0:
                if user[0] in room[0].users.all():
                    if data['type'] == 'chat_message':
                        # Save message to db
                        saved_message = await self.save_message(user[0], data['message'], room[0])
                        # Send message to room group
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chat_message',
                                'message': MessageSerializer(saved_message).data
                            }
                        )
                    elif data['type'] == 'fetch_messages':
                        messages = await self.get_messages(room[0])

                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'fetch_messages',
                                'messages': MessageSerializer(messages, many=True).data
                            }
                        )

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_uuid']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))