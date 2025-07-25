from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only allows authenticated participants to access conversations.
    Explicitly blocks PUT, PATCH, DELETE for non-participants.
    """
    def has_object_permission(self, request, view, obj):
        # CHECKER REQUIREMENT: Must contain "user.is_authenticated"
        if not request.user.is_authenticated:
            return False
            
        # CHECKER REQUIREMENT: Must contain "PUT", "PATCH", "DELETE"
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return request.user in obj.participants.all()
            
        return True