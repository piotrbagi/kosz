from django.db import models
from django.db.models import Q


class Team(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    team_logo = models.ImageField(blank=True, default='nn.jpg')

    def __str__(self):
        return str(self.name)

    def get_players(self):
        return self.player_set.all()

    def get_team_stats(self):
        return self.team_stat.all()

    def get_games(self):
        return Game.objects.filter(Q(home=self) | Q(away=self))

    def get_points(self):
        home = self.home.filter(finished=True)
        away = self.away.filter(finished=True)
        mp = home.count() + away.count()
        points = 0
        win = 0
        lose = 0
        score = 0
        lost = 0
        for h in home:
            score += h.score1
            lost += h.score2
            if h.winner():
                points += 2
                win += 1
            else:
                points += 1
                lose += 1
        for a in away:
            score += a.score2
            lost += a.score1
            if a.winner():
                points += 1
                lose += 1
            else:
                points += 2
                win += 1
        return {'win': win, 'lose': lose, 'score': score, 'lost': lost, 'points': points, 'mp': mp}


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    on_court = models.BooleanField(default=False)
    image = models.ImageField(blank=True, default='nn.jpg')

    def __str__(self):
        return f'{self.first_name} {self.last_name} #{self.number}'

    def get_player_stats(self):
        ps = self.playerstats_set.all()
        return ps.filter(MIN__gt=0)

    def get_all_points(self):
        tot = list(self.get_player_stats().values_list('PKT', flat=True))
        return sum(tot)

    def get_all_rebs(self):
        totd = list(self.get_player_stats().values_list('TREB', flat=True))
        return sum(totd)

    def get_all_ast(self):
        tot = list(self.get_player_stats().values_list('AST', flat=True))
        return sum(tot)

    def get_all_blk(self):
        tot = list(self.get_player_stats().values_list('BLK', flat=True))
        return sum(tot)

    def get_all_stl(self):
        tot = list(self.get_player_stats().values_list('STL', flat=True))
        return sum(tot)

    def get_all_to(self):
        tot = list(self.get_player_stats().values_list('TO', flat=True))
        return sum(tot)

    def get_all_min(self):
        tot = list(self.get_player_stats().values_list('MIN', flat=True))
        return sum(tot)

    def get_all_mp(self):
        tot = list(self.get_player_stats().values_list('MIN', flat=True))
        res = 0
        for m in tot:
            if m > 0:
                res += 1
        return res

    def get_points_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_points() / self.get_all_mp(), 1)

    def get_rebs_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_rebs() / self.get_all_mp(), 1)

    def get_asts_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_ast() / self.get_all_mp(), 1)

    def get_mins_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_min() / self.get_all_mp(), 1)

    def get_blks_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_blk() / self.get_all_mp(), 1)

    def get_stls_per_game(self):
        if self.get_all_mp() == 0: return 0
        return round(self.get_all_stl() / self.get_all_mp(), 1)


class Game(models.Model):
    round = models.IntegerField(default=1)
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    place = models.CharField(max_length=50)
    referee = models.CharField(max_length=50)
    data = models.DateField(blank=True, auto_now=False)
    hour = models.TimeField(blank=True, auto_now=False)
    time = models.IntegerField(default=600, blank=False)
    reset_time = models.IntegerField(default=0, blank=True)
    quarter = models.IntegerField(default=1, blank=True)
    ot_time = models.IntegerField(default=300, blank=True)
    reset_ot = models.IntegerField(default=0, blank=True)
    ot = models.IntegerField(default=0, blank=True)
    is_ot = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.home} {self.score1} : {self.score2} {self.away}'

    def winner(self):
        if self.finished:
            if self.score1 > self.score2:
                return True
            return False

    def get_teams_stats(self):
        return self.team_game.all()

    def get_players_stats(self):
        return self.player_game.all()


class Stats(models.Model):
    FTM = models.IntegerField(default=0)
    FTA = models.IntegerField(default=0)
    FGM = models.IntegerField(default=0)
    FGA = models.IntegerField(default=0)
    FGM_three = models.IntegerField(default=0)
    FGA_three = models.IntegerField(default=0)
    AST = models.IntegerField(default=0)
    STL = models.IntegerField(default=0)
    TO = models.IntegerField(default=0)
    BLK = models.IntegerField(default=0)
    OREB = models.IntegerField(default=0)
    DREB = models.IntegerField(default=0)
    TREB = models.IntegerField(default=0, blank=True)
    PF = models.IntegerField(default=0)
    MIN = models.IntegerField(default=0)
    PKT = models.IntegerField(default=0)
    Fouls = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def percent_FT(self):
        if self.FTA == 0:
            return 0
        return round((self.FTM/self.FTA)*100, 0)

    def percent_FG(self):
        if self.FGA == 0:
            return 0
        return round((self.FGM/self.FGA)*100, 0 )

    def percent_FG_three(self):
        if self.FGA_three == 0:
            return 0
        return round((self.FGM_three/self.FGA_three)*100, 0)

class PlayerStats(Stats):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_game', null=True)
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player_opponent')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player} {self.player.team} [Vs{self.opponent}] '

    class Meta:
        verbose_name_plural = 'Player stats'


class TeamStats(Stats):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='team_game', null=True)
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_opponent')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_stat')

    def __str__(self):
        return f'{self.team} Vs {self.opponent}'

    class Meta:
        verbose_name_plural = 'Team stats'














