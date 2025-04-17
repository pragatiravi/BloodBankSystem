from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from accounts.models import UserType
from donor.models import DonorProfile
from donor.forms import DonorRegistrationForm, DonorProfileUpdateForm
from user.models import BloodRequest
from user.utils import notify_requester_donor_available

def donor_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create donor profile
            donor_profile = DonorProfile.objects.create(
                user=user,
                blood_group=form.cleaned_data.get('blood_group'),
                age=form.cleaned_data.get('age'),
                gender=form.cleaned_data.get('gender'),
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'),
                state=form.cleaned_data.get('state'),
            )
            
            # Set user as donor
            user_type, created = UserType.objects.get_or_create(user=user)
            user_type.is_donor = True
            user_type.save()
            
            messages.success(request, f'Your donor account has been created! You can now log in.')
            return redirect('login')
    else:
        form = DonorRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Donor Registration'
    }
    return render(request, 'donor/register.html', context)

@login_required
def donor_dashboard(request):
    # Check if user is a donor
    try:
        user_type = UserType.objects.get(user=request.user)
        if not user_type.is_donor:
            messages.error(request, 'You are not authorized to access the donor dashboard.')
            return redirect('home')
    except UserType.DoesNotExist:
        messages.error(request, 'You are not authorized to access the donor dashboard.')
        return redirect('home')
    
    # Get donor profile
    try:
        donor_profile = DonorProfile.objects.get(user=request.user)
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Donor profile not found. Please contact administrator.')
        return redirect('home')
    
    # Get recent blood requests
    recent_requests = BloodRequest.objects.filter(
        Q(blood_group=donor_profile.blood_group) | 
        Q(city=donor_profile.city),
        status='Pending'  # Only show pending requests
    ).order_by('-request_date')[:5]
    
    context = {
        'title': 'Donor Dashboard',
        'donor': donor_profile,
        'recent_requests': recent_requests
    }
    return render(request, 'donor/dashboard.html', context)

@login_required
def donor_profile(request):
    # Check if user is a donor
    try:
        user_type = UserType.objects.get(user=request.user)
        if not user_type.is_donor:
            messages.error(request, 'You are not authorized to access the donor profile.')
            return redirect('home')
    except UserType.DoesNotExist:
        messages.error(request, 'You are not authorized to access the donor profile.')
        return redirect('home')
    
    # Get or create donor profile
    donor_profile, created = DonorProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'blood_group': 'O+',
            'age': 25,
            'gender': 'Male',
            'phone_number': '',
            'address': '',
            'city': '',
            'state': '',
        }
    )
    
    if request.method == 'POST':
        form = DonorProfileUpdateForm(request.POST, request.FILES, instance=donor_profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            
            # Check if availability status changed to available
            if 'is_available' in form.changed_data and updated_profile.is_available:
                # Notify users with matching blood requests
                matching_requests = BloodRequest.objects.filter(
                    blood_group=updated_profile.blood_group,
                    status='Pending'
                )
                
                for blood_request in matching_requests:
                    if blood_request.user:
                        notify_requester_donor_available(blood_request, updated_profile)
            
            updated_profile.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('donor_profile')
    else:
        form = DonorProfileUpdateForm(instance=donor_profile)
    
    context = {
        'title': 'Donor Profile',
        'form': form,
        'donor': donor_profile
    }
    return render(request, 'donor/profile.html', context)

@login_required
def view_blood_requests(request):
    # Check if user is a donor
    try:
        user_type = UserType.objects.get(user=request.user)
        if not user_type.is_donor:
            messages.error(request, 'You are not authorized to access this page.')
            return redirect('home')
    except UserType.DoesNotExist:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    # Get donor profile
    try:
        donor_profile = DonorProfile.objects.get(user=request.user)
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Donor profile not found. Please contact administrator.')
        return redirect('home')
    
    # Get blood requests matching donor's blood group or city
    blood_requests = BloodRequest.objects.filter(
        Q(blood_group=donor_profile.blood_group) | 
        Q(city=donor_profile.city)
    ).order_by('-request_date')
    
    context = {
        'title': 'Blood Requests',
        'blood_requests': blood_requests
    }
    return render(request, 'donor/blood_requests.html', context)

@login_required
def toggle_availability(request):
    """Toggle donor availability status"""
    # Check if user is a donor
    try:
        user_type = UserType.objects.get(user=request.user)
        if not user_type.is_donor:
            messages.error(request, 'You are not authorized to perform this action.')
            return redirect('home')
    except UserType.DoesNotExist:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    # Get donor profile
    try:
        donor_profile = DonorProfile.objects.get(user=request.user)
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Donor profile not found. Please contact administrator.')
        return redirect('home')
    
    # Toggle availability
    donor_profile.is_available = not donor_profile.is_available
    donor_profile.save()
    
    # If donor becomes available, notify users with matching blood requests
    if donor_profile.is_available:
        matching_requests = BloodRequest.objects.filter(
            blood_group=donor_profile.blood_group,
            status='Pending'
        )
        
        for blood_request in matching_requests:
            if blood_request.user:
                notify_requester_donor_available(blood_request, donor_profile)
    
    status = "available" if donor_profile.is_available else "unavailable"
    messages.success(request, f'You are now {status} for blood donation.')
    return redirect('donor_dashboard')
