from django.urls import path

from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),

    path('<int:id>/tournament-detail/',
         views.dashboard_tournament_detail, name='db_tournament_detail'),

    path('host-tournament/', views.Create_Tournament,
         name='db_create_tournament'),

    path('<int:id>/update-tournament/',
         views.dashboard_tournament_update, name='db_update_tournament'),

    path('<str:t>/registered-teams/',
         views.dashboard_tournament_teams, name='db_tournament_teams'),

    path('<int:id>/delete-tournament-db/',
         views.dashboard_tournament_delete, name='db_delete_tournament'),

    path('<str:tt>/<str:team_name>/detail/', views.dashboard_tournament_team_detail,
         name='db_tournament_team_detail'),

    path('<str:tournament>/<str:team_name>/confirm-delete/',
         views.remove_team, name='remove_team'),

    path('<user_id>/<int:tournament_id>/accept-registeration/',
         views.AcceptRegisteration, name='AcceptRegisteration'),

    path('<int:tournamentID>/standings/',
         views.final_standings, name='FinalStandings'),

    path('add-standings/<int:tournamentID>/',
         views.add_results, name='db_add_results'),
]
