# Generated by Django 3.2 on 2021-05-03 08:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bio', models.CharField(max_length=150)),
                ('DOB', models.DateField(default=datetime.date(1990, 1, 1))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ProfileUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowerSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(auto_now_add=True)),
                ('FollowedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FollowedUser', to='Profile.profile')),
                ('Follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Follower', to='Profile.profile')),
            ],
        ),
    ]