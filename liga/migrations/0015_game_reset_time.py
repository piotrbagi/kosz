# Generated by Django 3.2.2 on 2021-06-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0014_auto_20210625_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='reset_time',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
