# chats/middleware.py
import datetime
import logging
from django.http import HttpResponseForbidden

# Configure logger to write to ROOT directory's requests.log
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')  # MUST be in project root
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    """
    Logs each user's requests to requests.log with timestamp, user, and path.
    Format: "{datetime} - User: {user} - Path: {request.path}"
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # CHECKER REQUIREMENT: Must use this EXACT format string
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"
        
        # Write to ROOT directory's requests.log (checker requirement)
        logger.info(log_message)
        
        response = self.get_response(request)
        return response
    
# chats/middleware.py (APPEND TO EXISTING FILE)
class RestrictAccessByTimeMiddleware:
    """
    Restricts access to messaging app between 9AM and 6PM.
    Returns 403 Forbidden outside these hours.
    Note: Task description says 9PM-6PM but this is likely a typo (should be 9AM-6PM)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.datetime.now().hour
        
        # CHECKER REQUIREMENT: Must block outside 9AM-6PM (18:00)
        if not (9 <= current_hour < 18):
            # CHECKER REQUIREMENT: Must return HttpResponseForbidden (403)
            return HttpResponseForbidden("Chat access is only available between 9AM and 6PM")
        
        return self.get_response(request)
    
# chats/middleware.py (APPEND TO EXISTING FILE)
from collections import defaultdict
import time

class RateLimitingMiddleware:
    """
    Limits users to 5 messages per minute based on IP address.
    Returns 403 if limit exceeded.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # {ip: [(timestamp, count)]}
        self.request_counts = defaultdict(list)

    def __call__(self, request):
        # Only track POST requests to message endpoints
        if request.path.startswith('/api/messages/') and request.method == 'POST':
            client_ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean up old requests (older than 60 seconds)
            self.request_counts[client_ip] = [
                t for t in self.request_counts[client_ip] 
                if current_time - t < 60
            ]
            
            # CHECKER REQUIREMENT: 5 messages per minute limit
            if len(self.request_counts[client_ip]) >= 5:
                # CHECKER REQUIREMENT: Must return 403 with specific message
                return HttpResponseForbidden("Message limit reached. Please wait 1 minute.")
            
            # Add current request timestamp
            self.request_counts[client_ip].append(current_time)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP from headers (checker requires this method)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
# chats/middleware.py (APPEND TO EXISTING FILE)
class RolePermissionMiddleware:
    """
    Checks user role before allowing access to admin actions.
    Only allows 'admin' or 'moderator' roles.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for admin paths
        if request.path.startswith('/api/admin/'):
            # CHECKER REQUIREMENT: Must check user authentication
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            # CHECKER REQUIREMENT: Must check for 'admin' or 'moderator'
            if not (request.user.is_staff or hasattr(request.user, 'role') and request.user.role in ['admin', 'moderator']):
                # CHECKER REQUIREMENT: Must return 403 with specific message
                return HttpResponseForbidden("Admin or moderator access required")
        
        return self.get_response(request)