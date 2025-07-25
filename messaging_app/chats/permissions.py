# chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Ensures user is participant in conversation for:
    - Conversation objects (direct check)
    - Message objects (via conversation relationship)
    """
    def has_object_permission(self, request, view, obj):
        # Handle Message objects (have conversation relationship)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # Handle Conversation objects
        return request.user in obj.participants.all()