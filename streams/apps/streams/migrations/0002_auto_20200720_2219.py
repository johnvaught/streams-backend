# Generated by Django 3.0.5 on 2020-07-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='follows',
        ),
        migrations.AlterField(
            model_name='stream',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
