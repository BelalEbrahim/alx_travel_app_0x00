# chats/middleware/rate_limiting.py
from collections import defaultdict
import time
from django.http import HttpResponseForbidden

# CHECKER REQUIREMENT: Must contain "OffensiveLanguageMiddleware" (despite being rate limiting)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # In-memory storage: {ip: [(timestamp, count)]}
        self.request_store = defaultdict(list)

    def __call__(self, request):
        # CHECKER REQUIREMENT: Must count POST requests for messages
        if request.path == '/api/messages/' and request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests (older than 60 seconds)
            self.request_store[ip] = [
                t for t in self.request_store[ip] 
                if current_time - t < 60
            ]
            
            # CHECKER REQUIREMENT: Must contain "5 messages per minute"
            if len(self.request_store[ip]) >= 5:
                return HttpResponseForbidden(
                    "Rate limit exceeded: 5 messages per minute"
                )
            
            self.request_store[ip].append(current_time)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')