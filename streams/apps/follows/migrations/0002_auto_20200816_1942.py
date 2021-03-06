# Generated by Django 3.0.5 on 2020-08-17 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('follows', '0001_initial'),
        ('streams', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamfollow',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='streamfollow',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.Stream'),
        ),
        migrations.AddField(
            model_name='profilefollow',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='profilefollow',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.Stream'),
        ),
        migrations.AddConstraint(
            model_name='streamfollow',
            constraint=models.UniqueConstraint(condition=models.Q(is_deleted=False), fields=('stream', 'profile'), name='unique_stream_follow'),
        ),
        migrations.AddConstraint(
            model_name='profilefollow',
            constraint=models.UniqueConstraint(condition=models.Q(is_deleted=False), fields=('stream', 'profile'), name='unique_profile_follow'),
        ),
    ]
