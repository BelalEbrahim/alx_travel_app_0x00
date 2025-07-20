# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
    
    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj).order_by('sent_at')
        return MessageSerializer(messages, many=True).data

class CreateConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all(),
        pk_field=serializers.UUIDField()
    )
    
    class Meta:
        model = Conversation
        fields = ['participants']
    
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants")
        return value

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']