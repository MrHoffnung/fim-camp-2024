from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='profile_followers', blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}"

class Post(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication_date = models.DateTimeField("date published", auto_now=True)
    title = models.CharField(max_length=100, default="Ohne Titel")
    content = models.TextField()

class NewsletterSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    text = models.TextField()
    link = models.URLField()
    read = models.BooleanField(default=False)

