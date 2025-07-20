from django.urls import path
from . import template_views

urlpatterns = [
    path('', template_views.home_view, name='template_home'),
    path('login/', template_views.login_view, name='template_login'),
    path('register/', template_views.register_view, name='template_register'),
    path('dashboard/', template_views.dashboard_view, name='template_dashboard'),
    path('logout/', template_views.logout_view, name='template_logout'),
    path('password-reset/', template_views.password_reset_view, name='template_password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', template_views.password_reset_confirm_view, name='template_password_reset_confirm'),
]
