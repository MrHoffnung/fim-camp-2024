from django.contrib.auth.models import User
from blog.models import Notification, Post

def create_notification(user_id, source, text, link):
    user = User.objects.get(id=user_id)
    notification = Notification(
        user=user,
        source=source,
        text=text,
        link=link,
        read=False  # Standardwert, kann weggelassen werden
    )
    notification.save()
    return notification


