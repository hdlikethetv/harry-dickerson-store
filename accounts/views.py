from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('products:home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate checks if credentials are valid
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to 'next' parameter if it exists, otherwise home
            next_url = request.GET.get('next', 'products:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('products:home')


@login_required
def profile(request):
    """
    User profile page - only accessible when logged in.
    The @login_required decorator handles this automatically.
    """
    return render(request, 'accounts/profile.html')