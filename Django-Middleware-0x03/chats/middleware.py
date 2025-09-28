from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat app
    outside of allowed hours (6AM – 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Deny access if time is between 9PM (21) and 6AM (6)
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden(
                "Access to the chat is restricted between 9PM and 6AM."
            )

        # Continue normally if within allowed hours
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that limits chat messages per IP.
    Allows only 5 messages (POST requests) per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests per IP
        self.message_log = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if request.method == "POST" and "/messages" in request.path:
            now = time.time()
            window = 60  # 1 minute window
            limit = 5    # max messages per minute

            # Initialize if IP not seen before
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Keep only requests within the last minute
            self.message_log[ip] = [
                ts for ts in self.message_log[ip] if now - ts < window
            ]

            # Check if limit exceeded
            if len(self.message_log[ip]) >= limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: You can only send 5 messages per minute."
                )

            # Log this request
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")



class RolepermissionMiddleware:
    """
    Middleware to restrict access based on user role.
    Only users with role 'admin' or 'moderator' can perform restricted actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # Apply restriction only if user is authenticated
        if user and user.is_authenticated:
            # Check if restricted path
            if request.path.startswith("/api/"):  
                # If User model has a `role` attribute
                if not hasattr(user, "role") or user.role not in ["admin", "moderator"]:
                    return HttpResponseForbidden(" Access denied: You don’t have permission.")

        return self.get_response(request)

