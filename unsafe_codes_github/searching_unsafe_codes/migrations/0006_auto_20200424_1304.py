# Generated by Django 3.0.3 on 2020-04-24 10:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('searching_unsafe_codes', '0005_history_repository_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
