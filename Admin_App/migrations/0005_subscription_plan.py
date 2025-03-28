# Generated by Django 5.1.2 on 2024-12-31 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0004_cast'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription_plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('duration_days', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('streaming_quality', models.CharField(max_length=100)),
                ('advertisements', models.CharField(max_length=50)),
            ],
        ),
    ]
