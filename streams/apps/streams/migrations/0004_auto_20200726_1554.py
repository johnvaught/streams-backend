# Generated by Django 3.0.5 on 2020-07-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_followed_streams'),
        ('follows', '0007_auto_20200726_1554'),
        ('streams', '0003_stream_followed_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='followed_profiles',
            field=models.ManyToManyField(related_name='following_streams', through='follows.ProfileFollow', to='profiles.Profile'),
        ),
    ]