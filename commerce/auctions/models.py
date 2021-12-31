from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField()
    starting_bid=models.IntegerField()
    category=models.CharField(max_length=64)
    img_url=models.CharField(max_length=256)
    username=models.CharField(max_length=64, null=True)
    status=models.CharField(max_length=16, default="active")

    def __str__(self):
        return f"{self.username} {self.title} {self.description} {self.starting_bid} {self.category} {self.img_url} {self.status}"

class Bid(models.Model):
    item=models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="bid")
    username=models.CharField(max_length=64, default="None")
    bid=models.IntegerField(default=0, null=True)
    bid_id=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item} {self.username} {self.bid} {self.bid_id}"


class Comment(models.Model):
    username=models.CharField(max_length=64, null=True)
    item_id=models.IntegerField(null=True)
    comment=models.TextField(null=True)

    def __str__(self):
        return f"{self.username} {self.item_id} {self.comment}"

class Watchlist(models.Model):
    item=models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    username=models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.username} {self.item}"
