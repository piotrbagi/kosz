from django.shortcuts import render
from .models import Game, Team, Player, PlayerStats, TeamStats
from django.db.models import Q
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView, UpdateView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import GameForm
from django.contrib.auth.forms import UserCreationForm
from .mixins import SuperUserRequiredMixin

def mm(request):
    return render(request, 'liga/mm.html')


class CustomLoginView(LoginView):
    template_name = 'liga/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('liga:table')


class CreateUser(SuperUserRequiredMixin, FormView):
    form_class = UserCreationForm
    template_name = 'liga/create_user.html'
    success_url = reverse_lazy('liga:mm')

    def form_valid(self, form):
        user = form.save()
        return super(CreateUser, self).form_valid(form)


class CreateGame(LoginRequiredMixin, CreateView):
    form_class = GameForm
    template_name = 'liga/create_game.html'
    success_url = reverse_lazy('liga:fixtures')


class CreatePlayer(LoginRequiredMixin, CreateView):
    model = Player
    template_name = 'liga/create_player.html'
    fields = ['first_name', 'last_name', 'team', 'number', 'image']
    success_url = reverse_lazy('liga:players')


class CreateTeamPlayer(LoginRequiredMixin, CreateView):
    model = Player
    template_name = 'liga/create_team_player.html'
    fields = ['first_name', 'last_name', 'number', 'image']

    def get_success_url(self):
        return reverse_lazy('liga:team', kwargs={'team_id': self.kwargs['num']})

    def form_valid(self, form):
        form.instance.team = Team.objects.get(pk=self.kwargs['num'])
        return super(CreateTeamPlayer, self).form_valid(form)


class CreateTeam(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'liga/create_team.html'
    fields = '__all__'
    success_url = reverse_lazy('liga:teams')


class DeleteGame(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = 'liga/delete_game.html'
    context_object_name = 'game'

    def get_success_url(self):
        if self.kwargs['name'] == 'False':
            return reverse_lazy('liga:fixtures')
        elif self.kwargs['name'] == 'True':
            return reverse_lazy('liga:results')
        else:
            return reverse_lazy('liga:team', kwargs={'team_id': self.kwargs['name']})


class DeletePlayer(LoginRequiredMixin, DeleteView):
    model = Player
    template_name = 'liga/delete_player.html'
    context_object_name = 'player'

    def get_success_url(self):
        if self.kwargs['name'].isdigit():
            return reverse_lazy('liga:team', kwargs={'team_id': self.kwargs['name']})
        return reverse_lazy('liga:players')


class DeleteTeam(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'liga/delete_team.html'
    context_object_name = 'team'
    success_url = reverse_lazy('liga:teams')


class EditGame(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['round', 'place', 'referee', 'data']
    template_name = 'liga/edit_game.html'

    def get_success_url(self):
        if self.kwargs['name'].isdigit():
            return reverse_lazy('liga:team', kwargs={'team_id': self.kwargs['name']})
        return reverse_lazy('liga:fixtures')


class EditPlayer(LoginRequiredMixin, UpdateView):
    model = Player
    fields = ['team', 'number', 'image']
    template_name = 'liga/edit_player.html'
    success_url = reverse_lazy('liga:players')


@login_required()
def record(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    game = Game.objects.get(pk=game_id)
    teams_stats = game.get_teams_stats()
    players_stats = game.get_players_stats()
    home_players = players_stats.filter(player__team=game.home)
    away_players = players_stats.filter(player__team=game.away)
    home_team = teams_stats.get(team=game.home)
    away_team = teams_stats.get(team=game.away)
    if game.time % 60 < 10:
        sec = f'0{game.time % 60}'
    else:
        sec = f'{game.time % 60}'
    time =f'{game.time // 60}:{sec}'
    context = {'home_players': home_players, 'home_team': home_team, 'away_players': away_players,
               'away_team': away_team, 'game': game, 'time': time}
    return render(request, 'liga/game_record.html', context)


def results(request):
    results = Game.objects.filter(finished=True).order_by('round', 'data')
    rounds = {result.round for result in results}
    context = {'results': results, 'rounds': list(rounds)}
    return render(request, 'liga/results.html', context)


def game_details(request, *args, **kwargs):
    game_id = kwargs.get('num')
    game = Game.objects.get(pk=game_id)
    teams_stats = game.get_teams_stats()
    players_stats = game.get_players_stats()
    home_players = players_stats.filter(player__team=game.home)
    away_players = players_stats.filter(player__team=game.away)
    home_team = teams_stats.get(team=game.home)
    away_team = teams_stats.get(team=game.away)
    context = {'home_players': home_players, 'home_team': home_team, 'away_players': away_players,
               'away_team': away_team}
    return render(request, 'liga/game_details.html', context)


def fixtures(request):
    fixtures = Game.objects.filter(Q(finished=False)).order_by('round', 'data')
    rounds = set(fix.round for fix in fixtures)
    context = {'fixtures': fixtures, 'rounds': rounds}
    return render(request, 'liga/fixtures.html', context)


def teams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'liga/teams.html', context)


def team(request, team_id):
    team = Team.objects.get(pk=team_id)
    players = team.get_players().order_by('number')
    games = team.get_games().order_by('data')
    context = {'players': players, 'games': games, 'team': team}
    return render(request, 'liga/team.html', context)


def players(request):
    players = Player.objects.all().order_by('last_name')
    teams = Team.objects.all()
    context = {'players': players, 'teams': teams}
    return render(request, 'liga/players.html', context)


def player_stats(request, player_id):
    player = Player.objects.get(pk=player_id)
    stats = player.get_player_stats()
    stats = stats.order_by('game__data')
    context = {'stats': stats, 'player': player}
    return render(request, 'liga/player.html', context)


def top_players(request):
    players = Player.objects.all()
    point_list = [(player, player.get_all_points()) for player in players]
    point_list.sort(key=lambda x: x[1], reverse=True)
    pl = point_list[:5]
    reb_list = [(player, player.get_all_rebs()) for player in players]
    reb_list.sort(key=lambda x: x[1], reverse=True)
    rl = reb_list[:5]
    ast_list = [(player, player.get_all_ast()) for player in players]
    ast_list.sort(key=lambda x: x[1], reverse=True)
    al = ast_list[:5]
    blk_list = [(player, player.get_all_blk()) for player in players]
    blk_list.sort(key=lambda x: x[1], reverse=True)
    bl = blk_list[:5]
    stl_list = [(player, player.get_all_stl()) for player in players]
    stl_list.sort(key=lambda x: x[1], reverse=True)
    sl = stl_list[:5]
    context = {'top_points': pl, 'top_rebs': rl, 'top_asts': al, 'top_blks': bl, 'top_stls': sl}
    return render(request, 'liga/top.html', context)


def table(request):
    teams = Team.objects.all()
    res = []
    for team in teams:
        num = team.get_points()
        num['team'] = team.name
        res.append(num)
    res.sort(key=lambda x: (x['points'], -x['mp'], x['score']), reverse=True)
    print(res)
    return render(request, 'liga/table.html', {'result': res})


def get_out_player(request, *args, **kwargs):
    team_id = kwargs.get('team')
    team = Team.objects.get(pk=team_id)
    players_out = list(team.get_players().filter(on_court=True).values())
    player_in = list(team.get_players().filter(on_court=False).values())
    return JsonResponse({'player_out': players_out, 'player_in': player_in})


def save_stats(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    game = Game.objects.get(pk=game_id)
    if request.is_ajax():
        clock = (request.POST.get('timer')).split(':')
        time_record = int(clock[0]) * 60 + int(clock[-1])
        game.time = time_record
        mins = request.POST.get('mins')
        stat = (request.POST.get('stat')).split()
        value = request.POST.get('value')
        player_id = stat[-1]
        stat_name = stat[0]
        player = Player.objects.get(pk=player_id)
        ps = PlayerStats.objects.get(Q(game=game) & Q(player=player))
        team = ps.player.team
        gs = TeamStats.objects.get(Q(game=game) & Q(team=team))
        val = {}
        setattr(ps, stat_name, value)
        vala = getattr(gs, stat_name) + 1
        setattr(gs, stat_name, vala)
        check = ['FTM', 'FGM', 'FGM_three']
        edi = ['FTA', 'FGA', 'FGA_three']
        if stat_name in check:
            ps.PKT = int(ps.FTM) + int(ps.FGM) * 2 + int(ps.FGM_three) * 3
            qua = game.quarter - 1
            for num, ele in enumerate(check):
                if ele == stat_name:
                    fa = getattr(ps, edi[num]) + 1
                    setattr(ps, edi[num], fa)
                    ga = getattr(gs, edi[num]) + 1
                    setattr(gs, edi[num], ga)
                    p = getattr(gs, 'PKT') + num + 1
                    setattr(gs, 'PKT', p)
                    if team == game.home:
                        game.score1 = p
                    else:
                        game.score2 = p
                    val['name'] = f'{edi[num]} {player_id}'
                    val['pkt_id'] = f'PKT {player_id}'
                    val['pkt'] = ps.PKT
        if stat_name == 'OREB' or stat_name == 'DREB':
            ps.TREB = int(ps.DREB) + int(ps.OREB)
            gs.TREB += 1
            val['name'] = f'TREB {player_id}'
        if stat_name == 'PF' and int(value) > 4:
            val['faul_limit'] = f'{player.first_name} {player.last_name} ma 5 fauli'
        ps.save()
        gs.save()
        game.save()

        if stat_name in check:
            pot = game.score1 - game.score2
            if qua < 4:
                sec = game.reset_time - time_record + qua * game.reset_time
            else:
                sec = game.reset_ot - time_record + 4 * game.reset_time + game.ot * game.reset_ot
            print(request.session.get(str(game_id)))
            if request.session.has_key(str(game_id)):
                v = request.session.get(str(game_id))
                if v[-1][0] == sec:
                    v.pop
                    v.append([sec, pot])
                else:
                    v.append([sec, pot])
                request.session[str(game_id)] = v
            else:
                request.session[str(game_id)] = [[0, 0], [sec, pot]]
            print(request.session.get(str(game_id)))
        if val:
            val['done'] = True
        else:
            val['done'] = False
        data = []
        data.append(val)
        player_mins = json.loads(mins)
        for id, min in player_mins.items():
            pl = Player.objects.get(pk=id)
            pm = PlayerStats.objects.get(Q(game=game) & Q(player=pl))
            if pm.MIN != int(min):
                pm.MIN = int(min)
                pm.save()
        ts = TeamStats.objects.get(Q(game=game) & Q(team=team))
        ts = model_to_dict(ts)
        team_stats = []
        team_stats.append(ts)
        return JsonResponse({'data': data, 'team_stats': team_stats})
    return JsonResponse({'done': False})


def save_time(request, *args, **kwargs):
    game_id = kwargs.get('game')
    game = Game.objects.get(pk=game_id)
    if request.is_ajax():
        mins = request.POST.get('mins')
        timer = request.POST.get('timer')
    player_mins = json.loads(mins)
    timer = timer.split(':')
    tt = int(timer[0]) * 60 + int(timer[1])
    game.time = tt
    game.save()
    for id, min in player_mins.items():
        pl = Player.objects.get(pk=id)
        pm = PlayerStats.objects.get(Q(game=game) & Q(player=pl))
        if pm.MIN != int(min):
            pm.MIN = int(min)
            pm.save()
    teams = game.get_teams_stats()
    mm = sum(list(game.get_players_stats().values_list('MIN', flat=True)))/2
    for team in teams:
        team.MIN = mm
        team.save()
    return JsonResponse({'time': True})


def save_qua(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    game = Game.objects.get(pk=game_id)
    if request.is_ajax():
        mins = request.POST.get('mins')
        qua = request.POST.get('qua')
        game.quarter = int(qua)
    player_mins = json.loads(mins)
    for id, min in player_mins.items():
        pl = Player.objects.get(pk=id)
        pm = PlayerStats.objects.get(Q(game=game) & Q(player=pl))
        if pm.MIN != int(min):
            pm.MIN = int(min)
            pm.save()
    teams = game.get_teams_stats()
    mm = sum(list(game.get_players_stats().values_list('MIN', flat=True))) / 2
    for team in teams:
        team.MIN = mm
        team.save()
    reset = game.reset_time
    game.time = reset
    game.save()
    return JsonResponse({'time_reset': reset})


def edit(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    if request.is_ajax():
        game = Game.objects.get(pk=game_id)
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        stat = request.POST.get('stat')
        value = request.POST.get('value')
        player_stat = PlayerStats.objects.get((Q(game=game) & Q(player=player)))
        ts = TeamStats.objects.get(Q(game=game) & Q(team=player.team))
        before = getattr(player_stat, stat)
        setattr(player_stat, stat, value)
        di = int(before) - int(getattr(player_stat, stat))
        new = int(getattr(ts, stat)) - di
        setattr(ts, stat, new)
        check = ['FTM', 'FGM', 'FGM_three']
        edi = ['FTA', 'FGA', 'FGA_three']
        dic = {}
        if stat in check:
            player_stat.PKT = int(player_stat.FTM) + int(player_stat.FGM) * 2 + int(player_stat.FGM_three) * 3
            ts.PKT = int(ts.FTM) + int(ts.FGM) * 2 + int(ts.FGM_three) * 3
            for num, ele in enumerate(check):
                if ele == stat:
                    diff = int(before) - int(getattr(player_stat, stat))
                    test = getattr(player_stat, edi[num])
                    fa = getattr(ts, edi[num])
                    aff = int(test) - diff
                    ufa = int(fa) - diff
                    setattr(player_stat, edi[num], aff)
                    setattr(ts, edi[num], ufa)
                    dic['name2'] = f'{edi[num]} {player_id}'
                    dic['value2'] = aff
                    dic['ts_id2'] = f'{check[num]}  {ts.pk}'
                    fm = getattr(ts, check[num])
                    fa = getattr(ts, edi[num])
                    dic['ts_val2'] = f'{fm}/{fa}'
                    pkt = f'PKT {player_id}'
                    dic['pkt'] = pkt
                    dic['pkt_value'] = player_stat.PKT
                    dic['ts_pkt_id'] = f'PKT  {ts.pk}'
                    dic['ts_pkt_val'] = ts.PKT
        if stat == 'OREB' or stat == 'DREB':
            reb = getattr(player_stat, stat)
            dif = int(before) - int(reb)
            player_stat.TREB -= dif
            ts.TREB -= dif
            dic['treb_value'] = player_stat.TREB
            dic['treb'] = f'TREB {player_id}'
            dic['ts_treb_id'] = f'TREB  {ts.pk}'
            dic['ts_treb_val'] = ts.TREB
        player_stat.save()
        ts.save()
        dic['name1'] = f'{stat} {player_id}'
        dic['valu'] = int(value)
        dic['ts_id'] = f'{stat}  {ts.pk}'
        dic['ts_val'] = getattr(ts, stat)
        if stat in edi or stat in check:
            for num, ele in enumerate(edi):
                if ele == stat:
                    dic['ts_id'] = f'{check[num]}  {ts.pk}'
                    fm = getattr(ts, check[num])
                    fa = getattr(ts, stat)
                    dic['ts_val'] = f'{fm}/{fa}'
        data =[]
        data.append(dic)
        return JsonResponse({'data': data})
    return JsonResponse({'data': False})


def start_five(request, *args, **kwargs):
    players_ids = kwargs.get('list').split(',')
    players_ids = [int(p) for p in players_ids]
    team = Player.objects.get(pk=players_ids[0]).team
    reset = team.get_players().filter(on_court=True)
    for r in reset:
        r.on_court = False
        r.save()
    for p in players_ids:
        player = Player.objects.get(pk=p)
        player.on_court = True
        player.save()
    out = list(team.get_players().values())
    return JsonResponse({'data': out})


def search_player(request):
    if request.is_ajax():
        word = request.POST.get('word')
        if word == '':
            players = Player.objects.all().order_by('last_name')
        else:
            players = Player.objects.filter(Q(last_name__icontains=word) | Q(first_name__icontains=word)).\
                order_by('last_name')
        out = list(players.values())
        for num, player in enumerate(players):
            if request.user.is_authenticated:
                log = True
            else:
                log = False
            d = {'team': player.team.name, 'pkt': player.get_points_per_game(), 'reb': player.get_rebs_per_game(),
                 'ast': player.get_asts_per_game(), 'regis': log}
            d['delete_player'] = request.build_absolute_uri(reverse('liga:delete_player', args=[player.id, player.first_name]))
            d['edit_player'] = request.build_absolute_uri(reverse('liga:edit_player', args=[player.id, player.first_name]))
            d['player_url'] = request.build_absolute_uri(reverse('liga:player_stats', args=[player.id]))
            out[num].update(d)
        return JsonResponse({'data': out})
    return JsonResponse({'data': False})


def search_player_team(request, *args, **kwargs):
    team_id = kwargs.get('team_id')
    if team_id == 0:
        players = Player.objects.all().order_by('last_name')
    else:
        players = Team.objects.get(pk=team_id).get_players().order_by('last_name')
    players_data = list(players.values())
    for num, player in enumerate(players):
        if request.user.is_authenticated:
            log = True
        else:
            log = False
        d = {'t': player.team.name, 'pkt': player.get_points_per_game(), 'reb': player.get_rebs_per_game(),
             'ast': player.get_asts_per_game(), 'regis': log}
        d['delete_player'] = request.build_absolute_uri(reverse('liga:delete_player', args=[player.id, player.first_name]))
        d['edit_player'] = request.build_absolute_uri(reverse('liga:edit_player', args=[player.id, player.first_name]))
        d['player_url'] = request.build_absolute_uri(reverse('liga:player_stats', args=[player.id]))
        players_data[num].update(d)
    return JsonResponse({'data': players_data})


def res_round_games(request, *args, **kwargs):
    game_num = kwargs.get('round_num')
    if game_num == 0:
        games = Game.objects.filter(finished=True).order_by('round', 'data')
    else:
        games = Game.objects.filter(Q(round=game_num) & Q(finished=True))
    out = list(games.values())
    for num, game in enumerate(games):
        dat = out[num]
        dat['home'] = game.home.name
        dat['away'] = game.away.name
        if request.user.is_authenticated:
            log = True
        else:
            log = False
        dat['regis'] = log
        dat['delete_game'] = request.build_absolute_uri(reverse('liga:delete_game', args=[game.id, 'True']))
    return JsonResponse({'data': out})


def fix_round_games(request, *args, **kwargs):
    fix_num = kwargs.get('round_fix')
    if fix_num == 0:
        games = Game.objects.filter(finished=False).order_by('round', 'data')
    else:
        games = Game.objects.filter(Q(round=fix_num) & Q(finished=False))
    out = list(games.values())
    for num, game in enumerate(games):
        dat = out[num]
        dat['home'] = game.home.name
        dat['away'] = game.away.name
        if request.user.is_authenticated:
            log = True
        else:
            log = False
        dat['regis'] = log
        dat['delete_game'] = request.build_absolute_uri(reverse('liga:delete_game', args=[game.id, 'False']))
        dat['edit_game'] = request.build_absolute_uri(reverse('liga:edit_game', args=[game.id, game.away.name]))
        dat['record_game'] = request.build_absolute_uri(reverse('liga:record', args=[game.id]))
    return JsonResponse({'data': out})


def save_ot(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    game = Game.objects.get(pk=game_id)
    if request.is_ajax():
        mins = request.POST.get('mins')
        ot = request.POST.get('ot')
        game.ot = int(ot)
    player_mins = json.loads(mins)
    for id, min in player_mins.items():
        pl = Player.objects.get(pk=id)
        pm = PlayerStats.objects.get(Q(game=game) & Q(player=pl))
        if pm.MIN != int(min):
            pm.MIN = int(min)
            pm.save()
    teams = game.get_teams_stats()
    mm = sum(list(game.get_players_stats().values_list('MIN', flat=True))) / 2
    for team in teams:
        team.MIN = mm
        team.save()
    reset = game.reset_ot
    game.ot_time = reset
    game.save()
    return JsonResponse({'time_reset': reset})


def the_end(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    game = Game.objects.get(pk=game_id)
    if request.is_ajax():
        mins = request.POST.get('mins')
    player_mins = json.loads(mins)
    for id, min in player_mins.items():
        pl = Player.objects.get(pk=id)
        pm = PlayerStats.objects.get(Q(game=game) & Q(player=pl))
        if pm.MIN != int(min):
            pm.MIN = int(min)
            pm.save()
    teams = game.get_teams_stats()
    mm = sum(list(game.get_players_stats().values_list('MIN', flat=True))) / 2
    for team in teams:
        team.MIN = mm
        team.save()
    game.finished = True
    game.save()
    return JsonResponse({'done': True})


def game_chart(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    stat = request.session.get(str(game_id))
    return JsonResponse({'data': stat})