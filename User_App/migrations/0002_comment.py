# Generated by Django 5.1.2 on 2024-12-28 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0004_cast'),
        ('User_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', to='Admin_App.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User_App.viewers')),
            ],
        ),
    ]
