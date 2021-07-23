from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
app_name = 'liga'

urlpatterns = [
    path('', mm, name='mm'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('create_game', CreateGame.as_view(), name='create_game'),
    path('create_player', CreatePlayer.as_view(), name='create_player'),
    path('create_team_player/<int:num>', CreateTeamPlayer.as_view(), name='create_team_player'),
    path('create_team', CreateTeam.as_view(), name='create_team'),
    path('create_user', CreateUser.as_view(), name='create_user'),
    path('logout/', LogoutView.as_view(next_page='liga:table'), name='logout'),
    path('delete_game/<int:pk>/<str:name>', DeleteGame.as_view(), name='delete_game'),
    path('delete_player/<int:pk>/<str:name>/', DeletePlayer.as_view(), name='delete_player'),
    path('delete_team/<int:pk>/', DeleteTeam.as_view(), name='delete_team'),
    path('edit_game/<int:pk>/<str:name>', EditGame.as_view(), name='edit_game'),
    path('edit_player/<int:pk>/<str:name>/', EditPlayer.as_view(), name='edit_player'),
    path('record/<int:game_id>', record, name="record"),
    path('team/<int:team_id>/', team, name="team"),
    path('results/', results, name="results"),
    path('player/<int:player_id>/', player_stats, name="player_stats"),
    path('game/<int:num>/', game_details, name='game_stats'),
    path('fixtures/', fixtures, name='fixtures'),
    path('teams/', teams, name="teams"),
    path('players/', players, name="players"),
    path('get-out-players/<str:team>/', get_out_player, name='out_player'),
    path('save-stats/<int:game_id>/', save_stats, name='save_stats'),
    path('save-time/<int:game>', save_time, name='save_time'),
    path('save-qua/<int:game_id>', save_qua, name='save_qua'),
    path('save-ot/<int:game_id>', save_ot, name="save_ot"),
    path('the-end/<int:game_id>', the_end, name='the_end'),
    path('edit/<int:game_id>/', edit, name='edit'),
    path('start-five/<str:list>/', start_five, name='start_five'),
    path('top/', top_players, name='top'),
    path('table/', table, name='table'),
    path('search-player/', search_player, name='search_player'),
    path('search-player-team/<int:team_id>/', search_player_team, name='search_player_team'),
    path('res-round-games/<int:round_num>/', res_round_games, name='res_round_games'),
    path('fix-round-games/<int:round_fix>/', fix_round_games, name='fix_round_games'),
    path('game-chart/<int:game_id>', game_chart, name='game_chart')

]