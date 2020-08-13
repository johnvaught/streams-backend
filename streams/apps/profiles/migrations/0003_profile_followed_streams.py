# Generated by Django 3.0.5 on 2020-07-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0003_stream_followed_profiles'),
        ('follows', '0007_auto_20200726_1554'),
        ('profiles', '0002_remove_profile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed_streams',
            field=models.ManyToManyField(related_name='following_profiles', through='follows.StreamFollow', to='streams.Stream'),
        ),
    ]