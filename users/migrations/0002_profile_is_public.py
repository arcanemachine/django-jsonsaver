# Generated by Django 3.1.7 on 2021-02-24 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
