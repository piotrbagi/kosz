# Generated by Django 3.2.2 on 2021-06-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0010_game_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='data',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.IntegerField(default=600),
        ),
    ]
