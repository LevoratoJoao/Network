
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("profile/<int:poster_id>", views.profile_view, name="profile"),
    path("profile/<str:poster_name>", views.profile_view, name="profile"),
    path("follow/<int:profile_id>", views.follow_view, name="follow"),
    path("unfollow/<int:profile_id>", views.unfollow_view, name="unfollow")
]
