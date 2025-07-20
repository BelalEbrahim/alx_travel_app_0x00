# chats/tests.py
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User, Conversation, Message

class ModelTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            email='user2@example.com',
            password='password123'
        )
        
    def test_conversation_creation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        self.assertEqual(conversation.participants.count(), 2)
        
    def test_message_creation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        message = Message.objects.create(
            sender=self.user1,
            conversation=conversation,
            message_body='Hello world'
        )
        self.assertEqual(message.conversation, conversation)