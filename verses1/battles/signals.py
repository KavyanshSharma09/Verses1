from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginActivity


@receiver(user_logged_in)
def record_login(sender, user, request, **kwargs):
    ip = None
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    ua = request.META.get('HTTP_USER_AGENT', '')[:512]

    LoginActivity.objects.create(user=user, ip_address=ip, user_agent=ua)
