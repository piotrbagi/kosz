from django.contrib import admin
from .models import Game, Team, Player, TeamStats, PlayerStats


class GameLine(admin.TabularInline):
    model = Game
    fields = ['home', 'away', 'place', 'referee', 'data']


class PlayerLine(admin.TabularInline):
    model = Player
    fields = ['first_name', 'last_name', 'number', 'on_court']


class TeamLine(admin.ModelAdmin):
    inlines = [PlayerLine]

    class Meta:
        model = Team


admin.site.register(Team, TeamLine)
admin.site.register(Game)
admin.site.register(TeamStats)
admin.site.register(PlayerStats)