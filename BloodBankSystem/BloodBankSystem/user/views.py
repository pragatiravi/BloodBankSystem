from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from donor.models import DonorProfile
from bbadmin.models import ContactQuery
from user.models import BloodRequest, Notification
from user.forms import BloodRequestForm, DonorSearchForm
from user.utils import (
    notify_matching_donors, 
    notify_admin_new_request, 
    notify_requester_donor_available,
    notify_request_fulfilled
)

def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'user/home.html', context)

def about_us(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'user/about_us.html', context)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create contact query
        contact_query = ContactQuery.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact_us')
    
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'user/contact_us.html', context)

def donor_list(request):
    donors = DonorProfile.objects.filter(is_available=True)
    context = {
        'title': 'Donor List',
        'donors': donors
    }
    return render(request, 'user/donor_list.html', context)

def search_donor(request):
    form = DonorSearchForm(request.GET or None)
    donors = None
    
    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        city = form.cleaned_data.get('city')
        
        # Build query
        query = Q(is_available=True)
        if blood_group:
            query &= Q(blood_group=blood_group)
        if city:
            query &= Q(city__icontains=city)
        
        donors = DonorProfile.objects.filter(query)
    
    context = {
        'title': 'Search Donor',
        'form': form,
        'donors': donors
    }
    return render(request, 'user/search_donor.html', context)

def donor_detail(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk, is_available=True)
    context = {
        'title': 'Donor Detail',
        'donor': donor
    }
    return render(request, 'user/donor_detail.html', context)

def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.save()
            
            # Send real-time notifications
            notify_matching_donors(blood_request)
            notify_admin_new_request(blood_request)
            
            messages.success(request, 'Blood request submitted successfully! We will contact you soon.')
            return redirect('home')
    else:
        form = BloodRequestForm()
        
        # Pre-fill form if user is authenticated
        if request.user.is_authenticated:
            form.initial = {
                'requester_name': f"{request.user.first_name} {request.user.last_name}",
                'requester_email': request.user.email,
            }
    
    context = {
        'title': 'Request Blood',
        'form': form
    }
    return render(request, 'user/request_blood.html', context)

@login_required
def my_blood_requests(request):
    # Get blood requests by current user
    blood_requests = BloodRequest.objects.filter(
        requester_email=request.user.email
    ).order_by('-request_date')
    
    context = {
        'title': 'My Blood Requests',
        'blood_requests': blood_requests
    }
    return render(request, 'user/my_blood_requests.html', context)

@login_required
def blood_request_detail(request, pk):
    # First, try to get the blood request by ID
    try:
        blood_request = BloodRequest.objects.get(pk=pk)
        
        # Check if user is admin or staff
        if request.user.is_staff or request.user.is_superuser:
            # Admin users can view any blood request
            pass
        # Check if user is the requester
        elif blood_request.requester_email == request.user.email:
            # User is the requester, allow access
            pass
        # Check if user is a donor with matching blood group
        elif hasattr(request.user, 'donorprofile') and request.user.donorprofile.blood_group == blood_request.blood_group:
            # User is a donor with matching blood group, allow access
            pass
        else:
            # User is not authorized to view this blood request
            messages.error(request, "You are not authorized to view this blood request.")
            return redirect('my_blood_requests')
            
        context = {
            'title': 'Blood Request Detail',
            'blood_request': blood_request,
            'is_owner': blood_request.requester_email == request.user.email,
            'is_admin': request.user.is_staff or request.user.is_superuser,
            'is_matching_donor': hasattr(request.user, 'donorprofile') and request.user.donorprofile.blood_group == blood_request.blood_group
        }
        return render(request, 'user/blood_request_detail.html', context)
        
    except BloodRequest.DoesNotExist:
        messages.error(request, "The requested blood request does not exist.")
        return redirect('my_blood_requests')

@login_required
def notifications(request):
    """View for displaying user notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read if requested
    if request.GET.get('mark_all_read'):
        notifications.update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('notifications')
    
    context = {
        'title': 'My Notifications',
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count()
    }
    return render(request, 'user/notifications.html', context)

@login_required
def mark_notification_read(request, pk):
    """Mark a specific notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    # Redirect back to notifications page
    return redirect('notifications')
