# Generated by Django 4.2.19 on 2025-03-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_card_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration_month',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiration_year',
            field=models.CharField(max_length=4),
        ),
    ]
