# Generated by Django 5.0.3 on 2024-11-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_item_stateus'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='current_position',
            field=models.CharField(default='', max_length=100),
        ),
    ]
