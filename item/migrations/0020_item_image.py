# Generated by Django 5.0.3 on 2024-11-28 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0019_alter_item_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='img1.jpg', upload_to='images'),
        ),
    ]
