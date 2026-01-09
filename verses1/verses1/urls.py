from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from battles import views
from battles.auth_views import RateLimitedLoginView, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # For email verification and password reset
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', RateLimitedLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Problems
    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<slug:slug>/', views.problem_detail, name='problem_detail'),
    
    # Battles
    path('battle/create/', views.create_battle, name='create_battle'),
    path('battle/join/', views.join_battle, name='join_battle'),
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    path('battle/<int:battle_id>/result/', views.battle_result, name='battle_result'),
    path('battle/<int:battle_id>/status/', views.battle_status, name='battle_status'),
    path('battle/<int:battle_id>/run-tests/', views.run_tests, name='run_tests'),
    path('battle/<int:battle_id>/submit/', views.submit_code, name='submit_code'),
    path('battles/history/', views.battle_history, name='battle_history'),
    
    # Practice Mode
    path('practice/', views.practice, name='practice'),
    path('practice/<slug:slug>/', views.practice_problem, name='practice_problem'),
    path('practice/<slug:slug>/run-tests/', views.practice_run_tests, name='practice_run_tests'),
    path('practice/<slug:slug>/submit/', views.practice_submit, name='practice_submit'),
    path('practice/<slug:slug>/submissions/', views.submission_history, name='submission_history'),
    
    # Submissions
    path('submissions/', views.all_submissions, name='all_submissions'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    
    # User Profile
    path('profile/', views.user_profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    
    path('login-activity/', views.login_activity, name='login_activity'),
    path('api/analyze-preview/', views.analyze_code_preview, name='analyze_code_preview'),
    
    path('', include('upload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
