from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import secrets
import re
from urllib.parse import urlencode
import requests
from .middleware import check_rate_limit, increment_rate_limit, reset_rate_limit
from .forms import UserRegistrationForm
from .models import UserStats


def _normalize_provider_name(provider: str) -> str:
    aliases = {
        'google-oauth2': 'google',
        'google_oauth2': 'google',
        'googleoauth2': 'google',
    }
    return aliases.get((provider or '').strip().lower(), (provider or '').strip().lower())


class RateLimitedLoginView(DjangoLoginView):
    """Custom login view with rate limiting and remember me functionality"""
    
    def post(self, request, *args, **kwargs):
        # Check if user exceeded login attempts
        if check_rate_limit(request):
            messages.error(
                request,
                'Too many login attempts. Please try again in 15 minutes.'
            )
            return render(request, self.template_name, {'form': self.get_form()})
        
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Successful login
            login(request, user)
            reset_rate_limit(request)  # Reset failed attempts
            
            # Handle "Remember Me"
            if not remember_me:
                request.session.set_expiry(0)  # Expire on browser close
            else:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            # Failed login
            increment_rate_limit(request)
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name, {'form': self.get_form()})


def _safe_next_url(request, candidate: str) -> str:
    if candidate and url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return '/'


def _build_unique_username(seed: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9_.-]+', '_', (seed or 'operator')).strip('._-') or 'operator'
    clean = clean[:30]
    username = clean
    suffix = 1
    while User.objects.filter(username=username).exists():
        candidate = f"{clean[:24]}_{suffix}"
        username = candidate[:30]
        suffix += 1
    return username


@require_http_methods(["GET"])
def supabase_oauth_start(request, provider):
    supabase_url = (getattr(settings, 'SUPABASE_URL', '') or '').rstrip('/')
    supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '') or ''
    allowed_providers = {
        _normalize_provider_name(name)
        for name in getattr(settings, 'SUPABASE_OAUTH_PROVIDERS', ('google', 'github'))
    }
    provider = _normalize_provider_name(provider)

    if not supabase_url or not supabase_anon_key:
        missing = []
        if not supabase_url:
            missing.append('SUPABASE_URL (or NEXT_PUBLIC_SUPABASE_URL)')
        if not supabase_anon_key:
            missing.append('SUPABASE_ANON_KEY (or NEXT_PUBLIC_SUPABASE_ANON_KEY)')
        messages.error(request, f"Supabase OAuth is not configured yet. Missing: {', '.join(missing)}")
        return redirect('login')

    if provider not in allowed_providers:
        allowed_list = ', '.join(sorted(allowed_providers)) or 'google, github'
        messages.error(request, f'Unsupported OAuth provider. Allowed providers: {allowed_list}.')
        return redirect('login')

    request.session['supabase_oauth_next'] = _safe_next_url(request, request.GET.get('next', '/'))
    request.session['supabase_oauth_nonce'] = secrets.token_urlsafe(24)

    redirect_to = request.build_absolute_uri(reverse('supabase_oauth_callback'))
    authorize_url = f"{supabase_url}/auth/v1/authorize?{urlencode({'provider': provider, 'redirect_to': redirect_to})}"
    return redirect(authorize_url)


@require_http_methods(["GET"])
def supabase_oauth_callback(request):
    error = request.GET.get('error_description') or request.GET.get('error')
    if error:
        messages.error(request, f'Supabase OAuth error: {error}')
        return redirect('login')

    nonce = request.session.get('supabase_oauth_nonce')
    if not nonce:
        messages.error(request, 'OAuth session expired. Please try again.')
        return redirect('login')

    return render(
        request,
        'registration/supabase_callback.html',
        {
            'oauth_nonce': nonce,
            'complete_url': reverse('supabase_oauth_complete'),
        },
    )


@csrf_exempt
@require_http_methods(["POST"])
def supabase_oauth_complete(request):
    supabase_url = (getattr(settings, 'SUPABASE_URL', '') or '').rstrip('/')
    supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '') or ''

    if not supabase_url or not supabase_anon_key:
        return JsonResponse({'error': 'Supabase OAuth is not configured.'}, status=500)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    access_token = (payload.get('access_token') or '').strip()
    nonce = payload.get('nonce') or ''
    expected_nonce = request.session.get('supabase_oauth_nonce')

    if not access_token:
        return JsonResponse({'error': 'Missing access token.'}, status=400)
    if not expected_nonce or not nonce or not secrets.compare_digest(nonce, expected_nonce):
        return JsonResponse({'error': 'Invalid OAuth session.'}, status=403)

    # One-time nonce usage.
    request.session.pop('supabase_oauth_nonce', None)

    try:
        response = requests.get(
            f"{supabase_url}/auth/v1/user",
            headers={
                'Authorization': f'Bearer {access_token}',
                'apikey': supabase_anon_key,
            },
            timeout=15,
        )
    except requests.RequestException:
        return JsonResponse({'error': 'Unable to reach Supabase Auth.'}, status=502)

    if response.status_code != 200:
        return JsonResponse({'error': 'Supabase token validation failed.'}, status=401)

    user_data = response.json()
    email = (user_data.get('email') or '').strip().lower()
    if not email:
        return JsonResponse({'error': 'Supabase account does not include an email.'}, status=400)

    metadata = user_data.get('user_metadata') or {}
    name = (metadata.get('name') or '').strip()
    first_name = (metadata.get('given_name') or '').strip()
    last_name = (metadata.get('family_name') or '').strip()
    username_seed = (
        metadata.get('user_name')
        or metadata.get('preferred_username')
        or name
        or email.split('@')[0]
    )

    user = User.objects.filter(email__iexact=email).first()
    if not user:
        user = User.objects.create_user(
            username=_build_unique_username(str(username_seed)),
            email=email,
            password=User.objects.make_random_password(),
        )

    if first_name and not user.first_name:
        user.first_name = first_name
    if last_name and not user.last_name:
        user.last_name = last_name
    if name and not user.first_name and not user.last_name:
        parts = name.split()
        user.first_name = parts[0]
        if len(parts) > 1:
            user.last_name = ' '.join(parts[1:])
    user.save(update_fields=['first_name', 'last_name'])

    UserStats.objects.get_or_create(user=user)

    if not user.is_active:
        return JsonResponse({'error': 'This account is disabled.'}, status=403)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    redirect_url = request.session.pop('supabase_oauth_next', '/')
    return JsonResponse({'redirect_url': redirect_url})


@require_http_methods(["GET", "POST"])
def register(request):
    """User registration with email verification"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserStats for new user
            UserStats.objects.get_or_create(user=user)
            messages.success(
                request,
                'Registration successful! Check your email to verify your account.'
            )
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
