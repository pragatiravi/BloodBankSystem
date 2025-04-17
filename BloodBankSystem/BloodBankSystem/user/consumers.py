import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from accounts.models import UserType
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notifications_{self.user_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Send existing notifications on connect
        notifications = await self.get_notifications()
        await self.send(text_data=json.dumps({
            'type': 'notification_list',
            'notifications': notifications
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.dumps(text_data)
        message_type = text_data_json.get('type', '')
        
        if message_type == 'mark_read':
            notification_id = text_data_json.get('notification_id')
            if notification_id:
                await self.mark_notification_read(notification_id)
                
                # Send updated notifications
                notifications = await self.get_notifications()
                await self.send(text_data=json.dumps({
                    'type': 'notification_list',
                    'notifications': notifications
                }))

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']
        notification_type = event['notification_type']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'message': message,
            'notification_type': notification_type
        }))
    
    @database_sync_to_async
    def get_notifications(self):
        try:
            user = User.objects.get(id=self.user_id)
            notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
            return [
                {
                    'id': notification.id,
                    'message': notification.message,
                    'notification_type': notification.notification_type,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for notification in notifications
            ]
        except User.DoesNotExist:
            return []
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False
