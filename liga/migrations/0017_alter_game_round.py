# Generated by Django 3.2.2 on 2021-07-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0016_game_reset_ot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='round',
            field=models.IntegerField(),
        ),
    ]
