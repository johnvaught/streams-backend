# Generated by Django 3.0.5 on 2020-08-27 03:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20200824_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['-created_at', '-updated_at']},
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
