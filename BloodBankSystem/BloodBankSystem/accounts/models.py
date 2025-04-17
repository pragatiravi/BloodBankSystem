from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_donor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        if self.is_donor:
            return f"{self.user.username} - Donor"
        elif self.is_admin:
            return f"{self.user.username} - Admin"
        else:
            return f"{self.user.username} - User"

@receiver(post_save, sender=User)
def create_user_type(sender, instance, created, **kwargs):
    if created:
        UserType.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_type(sender, instance, **kwargs):
    instance.usertype.save()
