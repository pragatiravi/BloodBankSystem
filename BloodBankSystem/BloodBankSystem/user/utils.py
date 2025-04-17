from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.models import UserType
from .models import Notification
from donor.models import DonorProfile

def create_notification(user, message, notification_type, related_request=None, related_donor=None):
    """
    Create a notification and send it via WebSocket if possible
    """
    # Create notification in database
    notification = Notification.objects.create(
        user=user,
        message=message,
        notification_type=notification_type,
        related_request=related_request,
        related_donor=related_donor
    )
    
    # Send real-time notification via WebSocket
    channel_layer = get_channel_layer()
    room_group_name = f'notifications_{user.id}'
    
    try:
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'notification_message',
                'message': message,
                'notification_type': notification_type
            }
        )
    except Exception as e:
        # Log the error but don't fail if WebSocket is not available
        print(f"WebSocket notification error: {e}")
    
    return notification

def notify_matching_donors(blood_request):
    """
    Notify all donors with matching blood group about a new blood request
    """
    # Find donors with matching blood group
    matching_donors = DonorProfile.objects.filter(
        blood_group=blood_request.blood_group,
        is_available=True
    )
    
    # Create notifications for each matching donor
    for donor_profile in matching_donors:
        message = f"New blood request: {blood_request.units_required} units of {blood_request.blood_group} needed at {blood_request.hospital_name}, {blood_request.city}"
        create_notification(
            user=donor_profile.user,
            message=message,
            notification_type='blood_request',
            related_request=blood_request
        )

def notify_request_fulfilled(blood_request):
    """
    Notify the requester that their blood request has been fulfilled
    """
    message = f"Your blood request for {blood_request.units_required} units of {blood_request.blood_group} has been fulfilled"
    create_notification(
        user=blood_request.user,
        message=message,
        notification_type='request_fulfilled',
        related_request=blood_request
    )

def notify_admin_new_request(blood_request):
    """
    Notify all admin users about a new blood request
    """
    # Find all admin users
    admin_user_types = UserType.objects.filter(is_admin=True)
    
    for user_type in admin_user_types:
        message = f"New blood request: {blood_request.units_required} units of {blood_request.blood_group} needed at {blood_request.hospital_name}, {blood_request.city}"
        create_notification(
            user=user_type.user,
            message=message,
            notification_type='blood_request',
            related_request=blood_request
        )

def notify_requester_donor_available(blood_request, donor_profile):
    """
    Notify the requester that a matching donor is available
    """
    message = f"A matching donor for blood group {blood_request.blood_group} is now available for your request"
    create_notification(
        user=blood_request.user,
        message=message,
        notification_type='donor_available',
        related_request=blood_request,
        related_donor=donor_profile
    )
