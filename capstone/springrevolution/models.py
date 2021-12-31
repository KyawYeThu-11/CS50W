from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    subscribe = models.BooleanField(default=False)
    time_interval = models.IntegerField(null=True, blank=True, default=None)
    receiving_date = models.DateField(null=True, blank=True)

class Link(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=32)
    source = models.CharField(max_length=32)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    
    def serialize(self):
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "category": self.category,
            "source": self.source,
            "date":self.date
        }

    def __str__(self):
        return f"{self.name} {self.url} {self.description} {self.category} {self.source} {self.date}"

class Message(models.Model):
    creator = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self):
        return f"{self.creator} {self.message}"

    