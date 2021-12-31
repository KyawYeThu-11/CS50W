from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

path('accounts/login/', auth_views.LoginView.as_view()),
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("create_post", views.create_post, name="create_post"),
    path("follow", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("love/<int:post_id>", views.love_post, name="love_post"),
    path("saved_posts", views.saved_posts, name="saved_posts"),
    path("save/post/<int:post_id>", views.save_post, name="save_post"),
    path("unsave/post/<int:post_id>", views.unsave_post, name="unsave_post"),
]
