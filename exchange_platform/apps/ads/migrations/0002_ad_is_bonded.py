# Generated by Django 4.2.7 on 2025-05-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='is_bonded',
            field=models.BooleanField(default=False, verbose_name='Забронировано'),
        ),
    ]
