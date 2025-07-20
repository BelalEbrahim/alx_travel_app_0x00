# messaging_app/chats/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateConversationSerializer,
    CreateMessageSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        # Only show conversations where current user is a participant
        return Conversation.objects.filter(participants=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateConversationSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Ensure creator is always a participant
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    
    def get_queryset(self):
        # Only show messages in conversations where user is a participant
        return Message.objects.filter(
            conversation__participants=self.request.user
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMessageSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)