from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import UserRegistrationForm
from .middleware import check_rate_limit, increment_rate_limit, reset_rate_limit
from .models import UserStats


class RateLimitedLoginView(DjangoLoginView):
    """Django username/password login with rate limiting and remember me."""

    def post(self, request, *args, **kwargs):
        if check_rate_limit(request):
            messages.error(
                request,
                'Too many login attempts. Please try again in 15 minutes.',
            )
            return render(request, self.template_name, {'form': self.get_form()})

        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)

        user = authenticate(
            request,
            username=username_or_email,
            password=password,
        )
        if user is None:
            email_user = User.objects.filter(
                email__iexact=username_or_email,
            ).first()
            if email_user:
                user = authenticate(
                    request,
                    username=email_user.username,
                    password=password,
                )

        if user is not None:
            login(request, user)
            reset_rate_limit(request)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(30 * 24 * 60 * 60)
            return redirect(self.get_success_url())

        increment_rate_limit(request)
        messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, {'form': self.get_form()})


@require_http_methods(['GET', 'POST'])
def register(request):
    """Register a user with Django's built-in authentication system."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserStats.objects.get_or_create(user=user)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
