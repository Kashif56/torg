from django.db import models
from django.contrib.auth import get_user_model

from account.models import UserProfile

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    image = models.ImageField(upload_to='posts', blank=True, null=True)

    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.user.username
