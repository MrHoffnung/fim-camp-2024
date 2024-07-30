from django.contrib.auth.models import User
from blog.models import Follow, NewsletterSubscription

def has_user_followed(user: User, followed_user: User) -> bool:
    return Follow.objects.filter(user=user, followed_user=followed_user).exists()

def has_user_subscribed(user: User, subscribed_to: User) -> bool:
    return NewsletterSubscription.objects.filter(user=user, subscribed_to=subscribed_to).exists()

def has_user_liked_post(user: User, post_id: int) -> bool:
    return user.post_likes.filter(id=post_id).exists()