from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField


class Post(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    content = models.TextField(max_length=140, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    edited = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    @property
    def likes(self):
        return self.liked_by.count()

    def __str__(self):
        return f"Post {self.id} by {self.created_by.username}"
