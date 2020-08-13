# Generated by Django 3.0.5 on 2020-07-21 02:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('follows', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=15)),
                ('is_private', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('follows', models.ManyToManyField(related_name='streams', to='follows.Follow')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
