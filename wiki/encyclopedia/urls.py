from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"), #using the name leads to the path specified 
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
