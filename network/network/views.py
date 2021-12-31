import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Profile
from .util import get_paginator

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        redirect_url = request.POST.get("next")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if redirect_url == 'None':
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(redirect_url)
                
        else:
            return render(request, "network/login.html", {
                "page":"Login",
                "message": "Invalid username and/or password."
            })
    else:
        redirect_url = request.GET.get("next")
        return render(request, "network/login.html", {
            "page":"Login",
            "next":redirect_url
        })


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {
            "page":"Register"
        })


def index(request):
    posts = Post.objects.order_by("-timestamp").all()
    page_obj = get_paginator(request, posts)

    return render(request, "network/index.html", {
        "page":"Home",
        "page_obj":page_obj,
        "posts_count":posts.count()
    })


@login_required(login_url='/login')
def following(request):
    following = request.user.following.all()
    users=[]
    for profile in following:
        users.append(profile.user)

    posts = Post.objects.filter(post_owner__in=users).order_by("-timestamp").all()
    page_obj = get_paginator(request, posts)
    return render(request, "network/index.html", {
        "page":"Following",
        "page_obj":page_obj
    })

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(post_owner=user).order_by("-timestamp").all()
    page_obj = get_paginator(request, posts)

    return render(request, "network/index.html", {
        "page":"Profile",
        "user":user,
        "page_obj":page_obj
    })

def saved_posts(request):
    user = User.objects.get(username=request.user.username)
    posts = user.saved_posts.all()
    page_obj = get_paginator(request, posts)

    return render(request, "network/index.html", {
        "page":"Saved Posts",
        "page_obj":page_obj
    })

def create_post(request):
    post_owner = User.objects.get(username=request.user.username)
    message = request.POST.get("post")

    post = Post(post_owner=post_owner, message=message)
    post.save()

    return HttpResponseRedirect(reverse('index'))

@login_required
def follow(request):
    follower = User.objects.get(username=request.user.username)
    followee = User.objects.get(username=request.POST['followee'])
    action = request.POST["action"]

    if action == "follow":
        followee.user_profile.get().followers.add(follower)
    else:
        followee.user_profile.get().followers.remove(follower)            
    follower.save()
    
    follower_number = followee.user_profile.get().followers.count()
    return HttpResponseRedirect(reverse('profile', args=(followee.username,)))

def edit_post(request, post_id):
    if request.method == 'PUT':
        data=json.loads(request.body)
        message = data.get("message")

        post = Post.objects.get(id=post_id)
        post.message = message;
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error":"PUT request required."}, status=400)

def love_post(request, post_id):
    action = request.GET.get('action')
    post = Post.objects.get(id=post_id)
    
    if action == 'love':
        # for preventing user love twice very quickly
        if request.user in post.liked_by.all():
            return HttpResponse(post.love)
        else:
            post.love += 1
            post.liked_by.add(request.user)
    elif action == 'unlove':
        # for preventing user unlove twice very quickly
        if request.user not in post.liked_by.all():
            return HttpResponse(post.love)
        else:
            post.love -= 1
            post.liked_by.remove(request.user)
    post.save()
    return HttpResponse(post.love)

def save_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.saved_by.add(request.user)
    post.save()
    return HttpResponse(status=204)

def unsave_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.saved_by.remove(request.user)
    post.save()
    return HttpResponse(status=204)
