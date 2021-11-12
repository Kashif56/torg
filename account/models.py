from django.db import models
from django.contrib.auth import get_user_model
from core.models import Tournament, RegisteredTeams


User = get_user_model()


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='images', blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact = models.PositiveIntegerField(blank=True, null=True)

    organizer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    tournaments = models.ManyToManyField(Tournament, blank=True)
    registered_in_tournaments = models.ManyToManyField(
        Tournament, blank=True, related_name='registered_tournaments')

    followers = models.ManyToManyField(User, related_name='followers')
    followed_to = models.ManyToManyField(User, related_name='followed_to')

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField()
    followed = models.BooleanField(default=False)

    def __str__(self):
        return self.from_user.username
