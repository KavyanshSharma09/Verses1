from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .middleware import check_rate_limit, increment_rate_limit, reset_rate_limit
from .forms import UserRegistrationForm
from .models import UserStats


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
