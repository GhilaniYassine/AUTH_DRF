from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from .serializers import UserRegistrationSerializer


def home_view(request):
    """Home page with welcome message and navigation"""
    return render(request, 'authentication/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('template_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username first, then email
        user = authenticate(request, username=username, password=password)
        if not user:
            # Try with email
            try:
                user_obj = CustomUser.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! You have successfully logged in.')
            return redirect('template_dashboard')
        else:
            messages.error(request, 'Invalid username/email or password. Please try again.')
    
    return render(request, 'authentication/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('template_dashboard')
    
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password1'),
            'password_confirm': request.POST.get('password2')
        }
        
        # Basic validation
        if not all(data.values()):
            messages.error(request, 'All fields are required.')
            return render(request, 'authentication/register.html')
        
        if data['password'] != data['password_confirm']:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html')
        
        if len(data['password']) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'authentication/register.html')
        
        # Check if username exists
        if CustomUser.objects.filter(username=data['username']).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'authentication/register.html')
        
        # Check if email exists
        if CustomUser.objects.filter(email=data['email']).exists():
            messages.error(request, 'Email already registered. Please use a different email or try logging in.')
            return render(request, 'authentication/register.html')
        
        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            
            # Auto login after registration
            auth_login(request, user)
            messages.success(request, f'🎉 Account created successfully! Welcome to Beya Tech, {user.first_name}! You are now logged in.')
            return redirect('template_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}. Please try again.')
    
    return render(request, 'authentication/register.html')


@login_required
def dashboard_view(request):
    return render(request, 'authentication/dashboard.html')


@login_required
def logout_view(request):
    user_name = request.user.first_name or request.user.username
    auth_logout(request)
    messages.success(request, f'👋 Goodbye {user_name}! You have been logged out successfully.')
    return redirect('template_home')


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            current_site = get_current_site(request)
            reset_link = f"http://{current_site.domain}/password-reset-confirm/{uid}/{token}/"
            
            # For testing, just show success message
            messages.success(request, f'📧 Password reset link sent to {email}. Check your email to continue.')
            print(f"Password Reset Link: {reset_link}")  # For development testing
            
        except CustomUser.DoesNotExist:
            # Don't reveal if email exists or not for security
            messages.success(request, 'If an account with that email exists, a reset link has been sent.')
    
    return render(request, 'authentication/password_reset.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                
                if new_password1 != new_password2:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'authentication/password_reset_confirm.html')
                
                if len(new_password1) < 8:
                    messages.error(request, 'Password must be at least 8 characters long.')
                    return render(request, 'authentication/password_reset_confirm.html')
                
                user.set_password(new_password1)
                user.save()
                messages.success(request, '✅ Password has been reset successfully! You can now log in with your new password.')
                return redirect('template_login')
            
            return render(request, 'authentication/password_reset_confirm.html')
        else:
            messages.error(request, 'Invalid or expired reset link.')
            return redirect('template_password_reset')
            
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, 'Invalid reset link.')
        return redirect('template_password_reset')
