from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist
from .util import list_categories, generate_watched_items

error=None
success=False

def close(request, listing_id):
    item=Listing.objects.get(id=listing_id)
    item.status="close"
    item.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
def bid(request, listing_id):
    v_username=request.user.username
    v_bid=int(request.POST["bid"])

    v_item=Listing.objects.get(id=listing_id)
    bid=Bid.objects.get(item=v_item)
    global error
    global success

    if bid.bid_id==0:
        if v_bid<Listing.objects.get(id=listing_id).starting_bid:
            error="Your bid must be greater or equal to the starting bid."
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        if v_bid<=bid.bid:
            error="Your bid must be greater than the highest bid."
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    bid.username=v_username
    bid.bid=v_bid
    bid.bid_id += 1
    bid.save()
    success=True
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def category(request, item_category):
    listings=Listing.objects.filter(category=item_category).all()
    
    categories=list_categories() #from util.py

    item_list=generate_watched_items(request)#from util.py
    
    return render(request, "auctions/index.html", {
        "title":item_category,
        "listings":listings,
        "categories":categories,
        "item_list":item_list
    })

def watchlist(request):
    
    categories=list_categories()#from util.py

    watched_listings = Watchlist.objects.filter(username=request.user.username).all()

    return render(request, "auctions/watchlist.html", {
        "watched_listings":watched_listings,
        "categories":categories,
    })

def watchlist_manipulation(request, listing_id):
    condition = request.POST.get("condition")
    origin = request.POST.get("origin")

    if condition == "add":
        v_item=Listing.objects.get(id=listing_id)
        save = Watchlist(item=v_item, username=request.user.username)
        save.save()
        if origin == "listing":
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif origin == "index":
            return HttpResponseRedirect(reverse('index'))
        elif origin == "watchlist":
            return HttpResponseRedirect(reverse('watchlist'))
    elif condition == "remove":
        v_item=Listing.objects.get(id=listing_id)
        delete = Watchlist.objects.get(item=v_item, username=request.user.username)
        delete.delete()

        if origin == "listing":
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif origin == "index":
            return HttpResponseRedirect(reverse('index'))
        elif origin == "watchlist":
            return HttpResponseRedirect(reverse('watchlist'))


def add_comment(request, listing_id):
    v_comment = request.POST.get("comment")
    v_username=request.user.username
    comment=Comment(username=v_username, item_id=listing_id, comment=v_comment)
    comment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def listing(request, listing_id):
    item=Listing.objects.get(id=listing_id)
    bid=Bid.objects.get(item=item)
    objects=Watchlist.objects.filter(username=request.user.username).all()

    comments = Comment.objects.filter(item_id=listing_id).all()

    global error
    error_message=error
    error = None

    global success
    success_message=success
    success = False

    status_message=item.status

    for obj in objects:
        if obj.item==item:
            return render(request, "auctions/listing.html", {
                "item":item,
                "bid":bid,
                "listing_id":listing_id,
                "condition":"remove",
                "comments":comments,
                "error":error_message,
                "success":success_message,
                "status_message":status_message
            })

    return render(request, "auctions/listing.html", {
        "item":item,
        "bid":bid,
        "listing_id":listing_id,
        "condition":"add",
        "comments":comments,
        "error":error_message,
        "success":success_message,
        "status_message":status_message
    })

def create(request):
    if request.method=="POST":
        v_title=request.POST["title"]
        v_description=request.POST["description"]
        v_bid=request.POST["bid"]
        v_category=request.POST["category"]
        v_url=request.POST["url"]
        v_username=request.POST["username"]

        listing = Listing(title=v_title, description=v_description, starting_bid=v_bid, category=v_category, img_url=v_url, username=v_username)
        listing.save()
        bid=Bid(item=listing, username=listing.username, bid=0, bid_id=0)
        bid.save()
        return HttpResponseRedirect(reverse('index'))

    else:
        categories=list_categories() #from util.py
        return render(request, "auctions/create.html", {
            "categories":categories
        })

def index(request):
    listings = Listing.objects.all()
    categories=list_categories() #from util.py
    
    item_list=generate_watched_items(request)#from util.py

    return render(request, "auctions/index.html", {
        "listings":listings,
        "categories":categories,
        "item_list":item_list
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

