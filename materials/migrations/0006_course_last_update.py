# Generated by Django 4.2 on 2024-07-14 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_subscription_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Последнее обновление'),
        ),
    ]