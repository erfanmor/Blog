# Generated by Django 5.1.1 on 2024-10-15 20:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
