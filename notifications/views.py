from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def mark_read(request):
    request.user.notifications.update(read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))
