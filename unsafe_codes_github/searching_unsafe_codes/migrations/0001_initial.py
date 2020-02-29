# Generated by Django 3.0.3 on 2020-02-26 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('params', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='History_repositories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='searching_unsafe_codes.History')),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('path_to_token', models.CharField(max_length=15)),
                ('author', models.CharField(max_length=80)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unsafe_codes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string_code', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=150)),
                ('add_description', models.CharField(max_length=150)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='searching_unsafe_codes.Languages')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='searching_unsafe_codes.Statuses')),
            ],
        ),
        migrations.CreateModel(
            name='History_unsafe_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unsafe_code', models.TextField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='searching_unsafe_codes.History_repositories')),
            ],
        ),
        migrations.AddField(
            model_name='history_repositories',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='searching_unsafe_codes.Languages'),
        ),
    ]