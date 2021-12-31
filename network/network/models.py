from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} {self.email}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    followers = models.ManyToManyField(User, blank=True, related_name="following")

class Post(models.Model):
    post_owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="my_posts")
    message = models.TextField()
    love = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    saved_by = models.ManyToManyField(User, blank=True, related_name="saved_posts")

    def __str__(self):
        return f"{self.post_owner} {self.message} {self.love} {self.timestamp} {self.liked_by} {self.saved_by}"


