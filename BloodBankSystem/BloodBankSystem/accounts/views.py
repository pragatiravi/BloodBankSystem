from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from accounts.forms import (
    UserRegisterForm, UserUpdateForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
from accounts.models import UserType

def login_view(request):
    if request.user.is_authenticated:
        # Redirect based on user type
        try:
            user_type = UserType.objects.get(user=request.user)
            if user_type.is_admin:
                return redirect('admin_dashboard')
            elif user_type.is_donor:
                return redirect('donor_dashboard')
            else:
                return redirect('home')
        except UserType.DoesNotExist:
            return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect based on user type
                try:
                    user_type = UserType.objects.get(user=user)
                    if user_type.is_admin:
                        return redirect('admin_dashboard')
                    elif user_type.is_donor:
                        return redirect('donor_dashboard')
                    else:
                        return redirect('home')
                except UserType.DoesNotExist:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            
            # Redirect based on user type
            try:
                user_type = UserType.objects.get(user=request.user)
                if user_type.is_admin:
                    return redirect('admin_dashboard')
                elif user_type.is_donor:
                    return redirect('donor_dashboard')
                else:
                    return redirect('home')
            except UserType.DoesNotExist:
                return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Change Password'
    }
    return render(request, 'accounts/password_change.html', context)
