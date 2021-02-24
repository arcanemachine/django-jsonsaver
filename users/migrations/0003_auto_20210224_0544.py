# Generated by Django 3.1.7 on 2021-02-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='confirmation_code',
            new_name='activation_code',
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_public',
            field=models.BooleanField(default=False, help_text='If this setting is active, users can look up this profile based on your username and view all your public stores.', verbose_name='Make this profile public'),
        ),
    ]
