from django.db import models
from django.contrib.auth.models import User
from donor.models import BLOOD_GROUP_CHOICES

# Create your models here.

class BloodRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )
    
    requester_name = models.CharField(max_length=100)
    requester_email = models.EmailField()
    requester_phone = models.CharField(max_length=15)
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_required = models.PositiveIntegerField(default=1)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    reason = models.TextField(help_text="Reason for blood request")
    request_date = models.DateTimeField(auto_now_add=True)
    needed_by_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    attended_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_requests')
    attended_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-request_date']
        
    def __str__(self):
        return f"Blood Request - {self.blood_group} for {self.patient_name} ({self.status})"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('blood_request', 'Blood Request'),
        ('donor_available', 'Donor Available'),
        ('request_fulfilled', 'Request Fulfilled'),
        ('general', 'General Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    related_request = models.ForeignKey('BloodRequest', on_delete=models.CASCADE, null=True, blank=True)
    related_donor = models.ForeignKey('donor.DonorProfile', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.notification_type} - {self.message[:30]}"
    
    class Meta:
        ordering = ['-created_at']
