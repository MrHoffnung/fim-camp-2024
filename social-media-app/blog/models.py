from typing import Iterable
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='profile_followers', blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.profile_image:
            self._resize_profile_image()
    
    def _resize_profile_image(self) -> None:
        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
    

    

class Post(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication_date = models.DateTimeField("date published", auto_now=True)
    title = models.CharField(max_length=100, default="Ohne Titel")
    content = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='post_downvotes', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)

    def calculate_rating(self) -> int:
        return self.upvotes.count() - self.downvotes.count()
    
class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    text = models.TextField()
    link = models.URLField()
    read = models.BooleanField(default=False)

