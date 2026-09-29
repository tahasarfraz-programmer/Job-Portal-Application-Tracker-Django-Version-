def unread_notifications(request):
    if not request.user.is_authenticated:
        return {}
    qs = request.user.notifications.all()
    return {'notifications': qs[:8], 'unread_count': qs.filter(read=False).count()}
