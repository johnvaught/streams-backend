# Generated by Django 3.0.5 on 2020-07-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follows', '0004_auto_20200722_1341'),
        ('profiles', '0002_remove_profile_follows'),
        ('streams', '0002_auto_20200720_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='followed_profiles',
            field=models.ManyToManyField(related_name='streams_following', through='follows.ProfileFollow', to='profiles.Profile'),
        ),
    ]
