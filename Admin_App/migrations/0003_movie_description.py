# Generated by Django 5.1.2 on 2024-12-19 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0002_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(default='no description'),
        ),
    ]
