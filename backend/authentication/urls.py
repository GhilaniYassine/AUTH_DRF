from django.urls import path, include
from .views import (
    register, login, logout, profile, profile_update, 
    change_password, CustomTokenRefreshView
)

urlpatterns = [
    # API endpoints
    path('register/', register, name='api_register'),
    path('login/', login, name='api_login'),
    path('logout/', logout, name='api_logout'),
    path('profile/', profile, name='api_profile'),
    path('profile/update/', profile_update, name='api_profile_update'),
    path('change-password/', change_password, name='api_change_password'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='api_token_refresh'),
    
    # Template-based views for testing (under /auth/template/)
    path('template/', include('authentication.template_urls')),
]
