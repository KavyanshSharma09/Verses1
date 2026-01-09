from django.utils.decorators import decorator_from_middleware
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
import hashlib

# Rate limiting for login attempts
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW = 900  # 15 minutes in seconds


class RateLimitMiddleware:
    """Middleware to rate limit login attempts"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_login_attempt_key(request):
    """Generate a cache key for login attempts"""
    ip = get_client_ip(request)
    username = request.POST.get('username', '')
    return f"login_attempt_{ip}_{username}"


def check_rate_limit(request):
    """Check if user has exceeded login attempts"""
    key = get_login_attempt_key(request)
    attempts = cache.get(key, 0)
    return attempts >= MAX_LOGIN_ATTEMPTS


def increment_rate_limit(request):
    """Increment login attempt counter"""
    key = get_login_attempt_key(request)
    attempts = cache.get(key, 0)
    cache.set(key, attempts + 1, LOGIN_ATTEMPT_WINDOW)


def reset_rate_limit(request):
    """Reset login attempt counter on successful login"""
    key = get_login_attempt_key(request)
    cache.delete(key)


@receiver(user_login_failed)
def handle_login_failed(sender, credentials, request, **kwargs):
    """Handle failed login attempts"""
    increment_rate_limit(request)
