from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/watchlist_manipulation", views.watchlist_manipulation, name="watchlist_manipulation"),
    path("<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("index/<str:item_category>", views.category, name="category"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close, name="close")
]
