from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notification

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == notification.MESSAGE:
            return redirect('conversation', user_id=notification.created_by.id)
        elif notification.notification_type == notification.FOLLOWER:
            return redirect('chirperprofile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('chirperprofile', username=notification.to_user.username)
        elif notification.notification_type == Notification.MENTION:
            return redirect('chirperprofile', username=notification.created_by.username)
    
    return render(request, 'notification/notifications.html')