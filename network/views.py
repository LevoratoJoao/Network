import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import User, Posts, Followers


def index(request):
    posts = Posts.objects.order_by("-creationDate").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj
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

def profile_view(request, poster_name):
    isFollowing = False
    try:
        user = User.objects.get(username=poster_name)
        posts = Posts.objects.filter(poster=user).order_by("-creationDate")
    except:
        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        aux = Followers.objects.filter(follower=user, following=request.user).exists()
        if aux:
            isFollowing = True
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    if request.method == "GET":
        return render(request, "network/profile.html", {
            "profile": user,
            "posts": page_obj,
            "isFollowing": isFollowing
        })
    else:
        return HttpResponseRedirect(reverse("index"))

# @csrf_exempt
# @login_required
# def follow_view(request, profile_name):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST request required"}, status=400)
#     try:
#         Followers.objects.get_or_create(follower=User.objects.get(username=profile_name), following=request.user)
#     except:
#         return JsonResponse({"Error": "Could not follow"}, status=404)
#     return JsonResponse({"follow": True, "message": f"{request.user} is following {profile_name}"}, status=201)

# @csrf_exempt
# @login_required
# def unfollow_view(request, profile_name):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST request required"}, status=400)
#     try:
#         follow = Followers.objects.get(follower=User.objects.get(username=profile_name), following=request.user)
#     except Followers.DoesNotExist:
#         follow = None
#     if follow:
#         follow.delete()
#         return JsonResponse({"follow": False, "message": f"{request.user} is not following {profile_name}"}, status=201)
#     return JsonResponse({"Error": "Could not unfollow"}, status=404)

@login_required
def follow_view(request, profile_name):
    Followers.objects.get_or_create(follower=User.objects.get(username=profile_name), following=request.user)
    paginator = Paginator(Posts.objects.filter(poster=User.objects.get(username=profile_name),).order_by("-creationDate"), 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
            "profile": User.objects.get(username=profile_name),
            "posts": page_obj,
            "isFollowing": True
    })

@login_required
def unfollow_view(request, profile_name):
    try:
        follow = Followers.objects.get(follower=User.objects.get(username=profile_name), following=request.user)
    except Followers.DoesNotExist:
        follow = None
    if follow:
        follow.delete()
    paginator = Paginator(Posts.objects.filter(poster=User.objects.get(username=profile_name),).order_by("-creationDate"), 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
            "profile": User.objects.get(username=profile_name),
            "posts": page_obj,
            "isFollowing": True
    })

@login_required
def following_view(request, user_name):
    following = Followers.objects.filter(following=request.user)
    posts = Posts.objects.order_by("-creationDate").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "following": following,
        "posts": page_obj
    })

@csrf_exempt
@login_required
def edit_view(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    content = json.loads(request.body)["content"]
    if content == "":
        return JsonResponse({"Error": "post can't be empty"}, status=404)
    try:
        post = Posts.objects.get(pk=post_id)
        post.content = content
        post.save()
        return JsonResponse({"data": post.serialize(), "message": "Post edit"}, status=201)
    except Posts.DoesNotExist:
        return JsonResponse({"Error": "post not found"}, status=404)

@csrf_exempt
def like_view(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    data = json.loads(request.body)
    try:
        post = Posts.objects.get(pk=post_id)
        if data['like'] == 1:
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        post.save()
        return JsonResponse({"data": post.serialize(), "message": "Post liked"}, status=201)
    except Posts.DoesNotExist:
        return JsonResponse({"Error": "post not found"}, status=404)
