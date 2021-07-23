# Generated by Django 3.2.2 on 2021-07-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0018_alter_game_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='round',
            field=models.CharField(choices=[('i', 1), ('i', 2), ('i', 3), ('i', 4), ('i', 5), ('i', 6), ('i', 7), ('i', 8), ('i', 9), ('i', 10), ('i', 11), ('i', 12), ('i', 13), ('i', 14), ('i', 15), ('i', 16), ('i', 17), ('i', 18), ('i', 19), ('i', 20), ('i', 21), ('i', 22), ('i', 23), ('i', 24), ('i', 25), ('i', 26), ('i', 27), ('i', 28), ('i', 29), ('i', 30), ('i', 31), ('i', 32), ('i', 33), ('i', 34), ('i', 35), ('i', 36), ('i', 37), ('i', 38), ('i', 39), ('i', 40)], default='1', max_length=5),
        ),
        migrations.DeleteModel(
            name='Round',
        ),
    ]