# Generated by Django 4.2.19 on 2025-03-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='bin',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
