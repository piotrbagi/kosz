from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, PlayerStats, TeamStats, Player


# create teams stats model after game creation
@receiver(post_save, sender=Game)
def post_save_game_create_stats(sender, instance, created, **kwargs):
    if created:
        TeamStats.objects.create(team=instance.home, opponent=instance.away, game=instance)
        TeamStats.objects.create(team=instance.away, opponent=instance.home, game=instance)
        instance.reset_time = instance.time
        instance.reset_ot = instance.ot_time
        instance.save()


# create player stats model after team stats creation
@receiver(post_save, sender=TeamStats)
def post_save_player_create_stats(sender, instance, created, **kwargs):
    if created:
        gg = instance.game
        opp = instance.opponent
        players = instance.team.get_players()
        for p in players:
            if p.active:
                PlayerStats.objects.create(player=p, opponent=opp, game=gg)


# create new player stats after add new player to the game
@receiver(post_save, sender=Player)
def post_save_player_create_stats(sender, instance, created, **kwargs):
    if created:
        games = instance.team.get_games().filter(finished=False)
        for game in games:
            num = []
            for ps in game.get_players_stats():
                num.append(ps.player.pk)
            if game.home == instance.team:
                opp = game.away
            else:
                opp = game.home
            if instance.pk not in num:
                PlayerStats.objects.create(player=instance, game=game, opponent=opp)









