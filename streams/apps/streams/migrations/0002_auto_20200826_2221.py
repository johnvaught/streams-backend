# Generated by Django 3.0.5 on 2020-08-27 03:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
