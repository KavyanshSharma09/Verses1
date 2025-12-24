from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from battles import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('battle/create/', views.create_battle, name='create_battle'),
    path('battle/join/', views.join_battle, name='join_battle'),
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    path('battle/<int:battle_id>/result/', views.battle_result, name='battle_result'),
    path('battle/<int:battle_id>/status/', views.battle_status, name='battle_status'),
    path('battles/history/', views.battle_history, name='battle_history'),
    
    path('login-activity/', views.login_activity, name='login_activity'),
    
    path('', include('upload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
