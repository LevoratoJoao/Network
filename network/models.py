from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="poster")
    content = models.TextField(max_length=500)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, null=True, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "creationDate": self.creationDate.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count()
        }

class Followers:
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="poster")
