# Generated by Django 5.1.7 on 2025-04-07 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0004_alter_menu_menu_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_name',
            field=models.CharField(max_length=255),
        ),
    ]
