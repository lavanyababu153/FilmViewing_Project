# Generated by Django 5.1.2 on 2025-01-23 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_App', '0013_subscription_user_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription_user',
            name='payment_status',
        ),
    ]
