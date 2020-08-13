# Generated by Django 3.0.5 on 2020-07-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follows', '0006_auto_20200725_2051'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='profilefollow',
            name='unique_field_profile_stream',
        ),
        migrations.AlterUniqueTogether(
            name='streamfollow',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='profilefollow',
            constraint=models.UniqueConstraint(condition=models.Q(is_deleted=False), fields=('stream', 'profile'), name='unique_profile_follow'),
        ),
        migrations.AddConstraint(
            model_name='streamfollow',
            constraint=models.UniqueConstraint(condition=models.Q(is_deleted=False), fields=('stream', 'profile'), name='unique_stream_follow'),
        ),
    ]