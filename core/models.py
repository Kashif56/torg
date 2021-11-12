from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ckeditor.fields import RichTextField


User = get_user_model()
GAME_MODE_CHOICES = (
    ('Solo', 'Solo'),
    ('Duo', 'Duo'),
    ('Squad', 'Squad')
)

# Create your models here.


class Tournament(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    fee = models.FloatField(null=True, blank=True)
    prize_pool = models.PositiveIntegerField()
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    slots = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    last_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    last_updated = models.DateTimeField(null=True, blank=True)

    teams = models.ManyToManyField('RegisteredTeams', null=True, blank=True)
    comments = models.ManyToManyField('Comment', related_name='comments')
    likes = models.ManyToManyField(User, related_name='tournament_likes')

    results = models.ManyToManyField('Results', related_name='results')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:Tournament_Detail',  kwargs={
            'id': self.id
        })

    def get_registeration_url(self):
        return reverse('core:Register_Team',  kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('core:Update_Tournament',  kwargs={
            'id': self.id
        })

    def get_cancel_registeration_url(self):
        return reverse('core:Cancel_Registeration',  kwargs={
            'id': self.id
        })


class RegisteredTeams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30)
    team_number = models.CharField(max_length=14)

    player1_ign = models.CharField(max_length=20)

    player2_ign = models.CharField(max_length=20)

    player3_ign = models.CharField(max_length=20)

    player4_ign = models.CharField(max_length=20)

    player5_ign = models.CharField(max_length=20, null=True, blank=True)

    is_registered = models.BooleanField(default=False)
    date_registered = models.DateTimeField()

    def __str__(self):
        return self.team_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user.username


class Results(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name='tournament')
    team = models.ForeignKey(
        RegisteredTeams, on_delete=models.CASCADE, related_name='team')
    rank = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return self.tournament.title
