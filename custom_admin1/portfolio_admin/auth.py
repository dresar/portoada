from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url and next_url.strip():
                return redirect(next_url)
            return redirect('portfolio_admin:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'portfolio_admin/login.html')

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portfolio_admin:login')

def admin_required(view_func):
    """
    Decorator to ensure only staff or superusers can access admin views.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('portfolio_admin:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('portfolio_admin:login')
        return view_func(request, *args, **kwargs)
    return wrapper