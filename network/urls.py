
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("profile/<str:poster_name>", views.profile_view, name="profile"),
    path("follow/<str:profile_name>", views.follow_view, name="follow"),
    path("unfollow/<str:profile_name>", views.unfollow_view, name="unfollow"),
    path("<str:user_name>/following", views.following_view, name="following")
]
