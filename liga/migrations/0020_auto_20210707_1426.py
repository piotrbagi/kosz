# Generated by Django 3.2.2 on 2021-07-07 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liga', '0019_auto_20210707_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='liga',
        ),
        migrations.DeleteModel(
            name='Ligue',
        ),
    ]
