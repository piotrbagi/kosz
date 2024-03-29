# Generated by Django 3.2.2 on 2021-05-11 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_game', to='liga.game'),
        ),
        migrations.AddField(
            model_name='teamstats',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_game', to='liga.game'),
        ),
    ]
