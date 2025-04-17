from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserType

# Create your models here.

# Blood group choices
BLOOD_GROUP_CHOICES = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    profile_pic = models.ImageField(upload_to='donor_profiles/', null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    last_donation_date = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.blood_group})"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        # Ensure user is marked as donor in UserType
        try:
            user_type = UserType.objects.get(user=self.user)
            user_type.is_donor = True
            user_type.save()
        except UserType.DoesNotExist:
            UserType.objects.create(user=self.user, is_donor=True)
        
        super().save(*args, **kwargs)
