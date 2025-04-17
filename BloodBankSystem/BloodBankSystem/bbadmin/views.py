from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Count, Sum
from django.http import HttpResponse
import datetime
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from accounts.models import UserType
from bbadmin.models import BloodGroup, AdminProfile, ContactQuery
from bbadmin.forms import BloodGroupForm, AdminRegistrationForm, AdminProfileUpdateForm, ContactResponseForm
from django.contrib.auth.forms import AuthenticationForm
from donor.models import DonorProfile
from user.models import BloodRequest
from user.forms import BloodRequestUpdateForm

# Admin authorization decorator
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            user_type = UserType.objects.get(user=request.user)
            if not user_type.is_admin:
                messages.error(request, 'You are not authorized to access the admin panel.')
                return redirect('home')
        except UserType.DoesNotExist:
            messages.error(request, 'You are not authorized to access the admin panel.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login(request):
    if request.user.is_authenticated:
        try:
            user_type = UserType.objects.get(user=request.user)
            if user_type.is_admin:
                return redirect('admin_dashboard')
            else:
                messages.warning(request, 'You are not authorized to access the admin panel.')
                return redirect('home')
        except UserType.DoesNotExist:
            messages.warning(request, 'You are not authorized to access the admin panel.')
            return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if user is an admin
                try:
                    user_type = UserType.objects.get(user=user)
                    if user_type.is_admin:
                        login(request, user)
                        messages.success(request, f'Welcome back, Admin {user.first_name}!')
                        return redirect('admin_dashboard')
                    else:
                        messages.error(request, 'You are not authorized to access the admin panel.')
                        return redirect('home')  # Redirect non-admin users to home
                except UserType.DoesNotExist:
                    messages.error(request, 'You are not authorized to access the admin panel.')
                    return redirect('home')  # Redirect users without UserType to home
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'title': 'Admin Login'
    }
    return render(request, 'bbadmin/login.html', context)

def admin_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create admin profile
            admin_profile = AdminProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
            )
            
            # Set user as admin
            user_type, created = UserType.objects.get_or_create(user=user)
            user_type.is_admin = True
            user_type.save()
            
            messages.success(request, f'Your admin account has been created! You can now log in.')
            return redirect('admin_login')
    else:
        form = AdminRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Admin Registration'
    }
    return render(request, 'bbadmin/register.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    # Get statistics
    total_blood_groups = BloodGroup.objects.count()
    total_donors = DonorProfile.objects.count()
    total_blood_requests = BloodRequest.objects.count()
    total_contact_queries = ContactQuery.objects.count()
    
    # Get blood group stats
    blood_groups = BloodGroup.objects.all()
    
    # Get recent blood requests
    recent_requests = BloodRequest.objects.order_by('-request_date')[:5]
    
    # Get recent contact queries
    recent_queries = ContactQuery.objects.filter(is_read=False).order_by('-date_sent')[:5]
    
    context = {
        'title': 'Admin Dashboard',
        'total_blood_groups': total_blood_groups,
        'total_donors': total_donors,
        'total_blood_requests': total_blood_requests,
        'total_contact_queries': total_contact_queries,
        'blood_groups': blood_groups,
        'recent_requests': recent_requests,
        'recent_queries': recent_queries
    }
    return render(request, 'bbadmin/dashboard.html', context)

@login_required
@admin_required
def admin_profile(request):
    # Get or create admin profile
    admin_profile, created = AdminProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone_number': '',
            'address': '',
        }
    )
    
    if request.method == 'POST':
        form = AdminProfileUpdateForm(request.POST, request.FILES, instance=admin_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('admin_profile')
    else:
        form = AdminProfileUpdateForm(instance=admin_profile)
    
    context = {
        'title': 'Admin Profile',
        'form': form,
        'admin': admin_profile
    }
    return render(request, 'bbadmin/profile.html', context)

@login_required
@admin_required
def blood_group_list(request):
    blood_groups = BloodGroup.objects.all()
    context = {
        'title': 'Blood Groups',
        'blood_groups': blood_groups
    }
    return render(request, 'bbadmin/blood_group_list.html', context)

@login_required
@admin_required
def blood_group_add(request):
    if request.method == 'POST':
        form = BloodGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood group added successfully!')
            return redirect('blood_group_list')
    else:
        form = BloodGroupForm()
    
    context = {
        'title': 'Add Blood Group',
        'form': form
    }
    return render(request, 'bbadmin/blood_group_form.html', context)

@login_required
@admin_required
def blood_group_update(request, pk):
    blood_group = get_object_or_404(BloodGroup, pk=pk)
    if request.method == 'POST':
        form = BloodGroupForm(request.POST, instance=blood_group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood group updated successfully!')
            return redirect('blood_group_list')
    else:
        form = BloodGroupForm(instance=blood_group)
    
    context = {
        'title': 'Update Blood Group',
        'form': form
    }
    return render(request, 'bbadmin/blood_group_form.html', context)

@login_required
@admin_required
def blood_group_delete(request, pk):
    blood_group = get_object_or_404(BloodGroup, pk=pk)
    if request.method == 'POST':
        blood_group.delete()
        messages.success(request, 'Blood group deleted successfully!')
        return redirect('blood_group_list')
    
    context = {
        'title': 'Delete Blood Group',
        'blood_group': blood_group
    }
    return render(request, 'bbadmin/blood_group_confirm_delete.html', context)

@login_required
@admin_required
def donor_list(request):
    donors = DonorProfile.objects.all()
    context = {
        'title': 'Donors',
        'donors': donors
    }
    return render(request, 'bbadmin/donor_list.html', context)

@login_required
@admin_required
def donor_detail(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    context = {
        'title': 'Donor Detail',
        'donor': donor
    }
    return render(request, 'bbadmin/donor_detail.html', context)

@login_required
@admin_required
def donor_delete(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    if request.method == 'POST':
        user = donor.user
        donor.delete()
        user.delete()  # Delete the associated user as well
        messages.success(request, 'Donor deleted successfully!')
        return redirect('donor_list')
    
    context = {
        'title': 'Delete Donor',
        'donor': donor
    }
    return render(request, 'bbadmin/donor_confirm_delete.html', context)

@login_required
@admin_required
def contact_query_list(request):
    queries = ContactQuery.objects.all()
    context = {
        'title': 'Contact Queries',
        'queries': queries
    }
    return render(request, 'bbadmin/contact_query_list.html', context)

@login_required
@admin_required
def contact_query_detail(request, pk):
    query = get_object_or_404(ContactQuery, pk=pk)
    
    # Mark as read if not read
    if not query.is_read:
        query.is_read = True
        query.save()
    
    if request.method == 'POST':
        form = ContactResponseForm(request.POST, instance=query)
        if form.is_valid():
            response = form.save(commit=False)
            response.responded_by = request.user
            response.responded_date = timezone.now()
            response.save()
            messages.success(request, 'Response sent successfully!')
            return redirect('contact_query_list')
    else:
        form = ContactResponseForm(instance=query)
    
    context = {
        'title': 'Contact Query Detail',
        'query': query,
        'form': form
    }
    return render(request, 'bbadmin/contact_query_detail.html', context)

@login_required
@admin_required
def contact_query_delete(request, pk):
    query = get_object_or_404(ContactQuery, pk=pk)
    if request.method == 'POST':
        query.delete()
        messages.success(request, 'Contact query deleted successfully!')
        return redirect('contact_query_list')
    
    context = {
        'title': 'Delete Contact Query',
        'query': query
    }
    return render(request, 'bbadmin/contact_query_confirm_delete.html', context)

@login_required
@admin_required
def blood_request_list(request):
    requests = BloodRequest.objects.all()
    context = {
        'title': 'Blood Requests',
        'requests': requests
    }
    return render(request, 'bbadmin/blood_request_list.html', context)

@login_required
@admin_required
def blood_request_detail(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    if request.method == 'POST':
        form = BloodRequestUpdateForm(request.POST, instance=blood_request)
        if form.is_valid():
            updated_request = form.save(commit=False)
            updated_request.attended_by = request.user
            updated_request.attended_date = timezone.now()
            
            # Check if status changed to Fulfilled
            if 'status' in form.changed_data and updated_request.status == 'Fulfilled':
                # Notify the requester
                from user.utils import notify_request_fulfilled
                if updated_request.user:
                    notify_request_fulfilled(updated_request)
            
            updated_request.save()
            messages.success(request, 'Blood request updated successfully!')
            return redirect('admin_blood_request_list')
    else:
        form = BloodRequestUpdateForm(instance=blood_request)
    
    context = {
        'title': 'Blood Request Detail',
        'blood_request': blood_request,
        'form': form
    }
    return render(request, 'bbadmin/blood_request_detail.html', context)

@login_required
@admin_required
def blood_request_delete(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, 'Blood request deleted successfully!')
        return redirect('blood_request_list')
    
    context = {
        'title': 'Delete Blood Request',
        'blood_request': blood_request
    }
    return render(request, 'bbadmin/blood_request_confirm_delete.html', context)

@login_required
@admin_required
def blood_request_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        report_format = request.POST.get('report_format', 'html')
        
        # Convert string dates to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Query blood requests within date range
        blood_requests = BloodRequest.objects.filter(
            request_date__date__gte=start_date,
            request_date__date__lte=end_date
        ).order_by('-request_date')
        
        if report_format == 'csv':
            # Generate CSV report
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="blood_requests_{start_date}_to_{end_date}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['ID', 'Requester Name', 'Patient Name', 'Blood Group', 
                            'Units Required', 'Hospital', 'City', 'Request Date', 'Status'])
            
            for request in blood_requests:
                writer.writerow([
                    request.id,
                    request.requester_name,
                    request.patient_name,
                    request.blood_group,
                    request.units_required,
                    request.hospital_name,
                    request.city,
                    request.request_date.strftime('%Y-%m-%d'),
                    request.status
                ])
            
            return response
        elif report_format == 'pdf':
            # Generate PDF report
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="blood_requests_{start_date}_to_{end_date}.pdf"'
            
            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []
            
            styles = getSampleStyleSheet()
            title = Paragraph(f"Blood Request Report ({start_date} to {end_date})", styles['Heading1'])
            elements.append(title)
            
            data = [['ID', 'Requester Name', 'Patient Name', 'Blood Group', 
                    'Units', 'Hospital', 'City', 'Request Date', 'Status']]
            
            for request in blood_requests:
                data.append([
                    str(request.id),
                    request.requester_name,
                    request.patient_name,
                    request.blood_group,
                    str(request.units_required),
                    request.hospital_name,
                    request.city,
                    request.request_date.strftime('%Y-%m-%d'),
                    request.status
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            return response
        else:
            # HTML report
            context = {
                'title': 'Blood Request Report',
                'blood_requests': blood_requests,
                'start_date': start_date,
                'end_date': end_date
            }
            return render(request, 'bbadmin/blood_request_report.html', context)
    
    context = {
        'title': 'Generate Blood Request Report'
    }
    return render(request, 'bbadmin/blood_request_report_form.html', context)
