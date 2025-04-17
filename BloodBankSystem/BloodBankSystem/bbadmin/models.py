from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserType

# Create your models here.

class BloodGroup(models.Model):
    name = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True, null=True)
    total_units = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    profile_pic = models.ImageField(upload_to='admin_profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        # Ensure user is marked as admin in UserType
        try:
            user_type = UserType.objects.get(user=self.user)
            user_type.is_admin = True
            user_type.save()
        except UserType.DoesNotExist:
            UserType.objects.create(user=self.user, is_admin=True)
        
        super().save(*args, **kwargs)

class ContactQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    responded_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_sent']
    
    def __str__(self):
        return f"{self.subject} from {self.name}"
