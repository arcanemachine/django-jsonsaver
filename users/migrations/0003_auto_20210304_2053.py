# Generated by Django 3.1.7 on 2021-03-05 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210301_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_public',
            field=models.BooleanField(default=False, help_text='If this setting is active, users can look up this profile via your username and view all your public JSON stores.', verbose_name='Make this profile publicly accessible'),
        ),
    ]