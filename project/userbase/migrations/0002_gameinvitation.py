# Generated by Django 5.0.2 on 2024-03-22 17:44

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamelist', '0002_requestedcategory_requestedmechanic'),
        ('userbase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_players', models.IntegerField(default=1)),
                ('game_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('game_place', models.CharField(max_length=64)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamelist.game')),
                ('players', models.ManyToManyField(blank=True, related_name='invited_players', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
