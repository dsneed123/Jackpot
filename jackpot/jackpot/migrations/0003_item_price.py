# Generated by Django 5.2 on 2025-04-22 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jackpot', '0002_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
