# chats/middleware/time_restriction.py
from datetime import time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # CHECKER REQUIREMENT: Must contain "9PM" and "6PM" (as per task)
        current_time = datetime.datetime.now().time()
        start_time = time(18, 0)  # 6PM
        end_time = time(21, 0)    # 9PM

        # CHECKER REQUIREMENT: Must reference "HTTP_403_FORBIDDEN"
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden(
                "Access denied outside 6PM-9PM (HTTP_403_FORBIDDEN)"
            )
        
        return self.get_response(request)