from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.Home, name='Home'),
    path('tournaments/', views.Tournaments, name='Tournaments'),
    path('tournaments/<str:query>/',
         views.TournamentQueryView, name='TournamentQuery'),


    path('<int:id>/tournament-detail/',
         views.Tournament_Detail, name='Tournament_Detail'),

    path('<int:id>/register_team/', views.RegisterTeam, name='Register_Team'),
    path('<int:id>/cancel-registeration/',
         views.CancelRegisteration, name='Cancel_Registeration'),
    path('about-us/', views.about_us, name='about-us'),

    path('<int:tournament_id>/registered-teams/',
         views.RegisteredTeamsView, name='RegisteredTeams'),


    path('like-tournament/<int:tournamentID>/',
         views.LikeTournament, name='LikeTournament'),
    path('add-comment/<int:tournamentID>/',
         views.AddComment, name='AddComment'),

    path('delete/<int:tournamentID>/<int:commentID>/',
         views.delete_comment, name='DeleteComment'),

    path('final-standings/<int:tournamentID>/',
         views.final_standings, name='Standings'),
]
