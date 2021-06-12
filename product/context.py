from product.models import Notification
from datetime import datetime
now = datetime.now()


def notification_context_processor(request):
    context = dict()
    try:
        if request.user.user_type == 'user':
            context['notifications_seen'] = Notification.objects.filter(created__month=now.month, client__user=request.user, seen=False)
            context['notifications'] = Notification.objects.filter(created__month=now.month, client__user=request.user)
        if request.user.user_type == 'vendor':
            context['notifications_seen'] = Notification.objects.filter(created__month=now.month, vendor__user=request.user, seen=False)
            context['notifications'] = Notification.objects.filter(created__month=now.month, vendor__user=request.user)
        if request.user.user_type == 'admin':
            context['notifications_seen'] = Notification.objects.filter(created__month=now.month, seen=False)
            context['notifications'] = Notification.objects.filter(created__month=now.month)
    except Exception:
        pass
    return context