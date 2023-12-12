# middleware.py
from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.utils import timezone

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity is not None:
                time_since_last_activity = timezone.now() - last_activity
                session_timeout = get_user_model().SESSION_COOKIE_AGE
                if time_since_last_activity.total_seconds() > session_timeout:
                    logout(request)
            request.session['last_activity'] = timezone.now()
        response = self.get_response(request)
        return response