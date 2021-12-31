from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist

class ListingAdmin(admin.ModelAdmin):
    list_display=("username", "title", "description", "starting_bid", "category", "img_url", "status")

class WatchlistAdmin(admin.ModelAdmin):
    list_display=("username", "item")

class CommentAdmin(admin.ModelAdmin):
    list_display=("username", "item_id", "comment")

class BidAdmin(admin.ModelAdmin):
    list_display=("item", "username", "bid", "bid_id")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)