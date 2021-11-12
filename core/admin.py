from django.contrib import admin
from .models import Tournament, RegisteredTeams, Comment, Results
# Register your models here.


class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'title', 'is_active'
    ]


class RegisteredTeamsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'team_name', 'team_number', 'is_registered'
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tournament', 'timestamp'
    ]


class ResultsAdmin(admin.ModelAdmin):
    list_display = [
        'tournament', 'team', 'rank'
    ]


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(RegisteredTeams, RegisteredTeamsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Results, ResultsAdmin)
