from .models import User, Listing, Bid, Comment, Watchlist

def list_categories():
    listings=Listing.objects.all()
    categories=set()
    for listing in listings:
        categories.add(listing.category)
    return categories

def generate_watched_items(request):
    watched_listings = Watchlist.objects.filter(username=request.user.username).all()
    item_list=[]
    for listing in watched_listings:
        item_list.append(listing.item)
    return item_list