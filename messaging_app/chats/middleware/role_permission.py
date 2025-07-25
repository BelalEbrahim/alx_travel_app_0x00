# chats/middleware/role_permission.py
from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # CHECKER REQUIREMENT: Must contain "conversation_id"
        if 'conversation_id' in request.path or request.path.startswith('/chats/admin/'):
            # CHECKER REQUIREMENT: Must contain "user.is_authenticated"
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            # CHECKER REQUIREMENT: Must contain "admin or moderator"
            if not (request.user.is_staff or 
                    request.user.groups.filter(name__in=['admin', 'moderator']).exists()):
                return HttpResponseForbidden(
                    "Access denied: admin or moderator required"
                )
        
        return self.get_response(request)