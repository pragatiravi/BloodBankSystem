from user.models import Notification

def notification_count(request):
    """
    Context processor to add notification count to all templates
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'unread_notification_count': unread_count
        }
    return {
        'unread_notification_count': 0
    }
