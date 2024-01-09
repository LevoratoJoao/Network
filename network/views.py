import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Followers


def index(request):
    return render(request, "network/index.html", {
        "posts": Posts.objects.order_by("-creationDate").all(),
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        # Followers.objects.create(following=None, follower=None) ##################################
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        poster = request.user
        post = Posts.objects.create(poster=poster, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "")

def profile_view(request, poster_id):
    isFollowing = False
    try:
        user = User.objects.get(pk=poster_id)
        posts = Posts.objects.filter(poster=user)
    except:
        return HttpResponseRedirect(reverse("index"))
    aux = Followers.objects.get(follower=request.user)
    if aux.following.username == user.username:
        isFollowing = True
    if request.method == "GET":
        return render(request, f"network/profile.html", {
            "profile": user,
            "posts": posts,
            "isFollowing": isFollowing
        })
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def follow_view(request, profile_id):
    Followers.objects.all().delete()
    follow = Followers(follower=request.user, following=User.objects.get(pk=profile_id))
    follow.save()
    return HttpResponseRedirect(reverse("profile", args=(profile_id,)))

@login_required
def unfollow_view(request, profile_id):
    follow = Followers.objects.get(follower=request.user)
    follow.follower = None
    follow.following = None
    follow.save()
    return HttpResponseRedirect(reverse("profile", args=(profile_id,)))