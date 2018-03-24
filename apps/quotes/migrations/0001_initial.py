# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-23 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('quote', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favr_id', models.ManyToManyField(related_name='favorites', to='main.User')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='main.User')),
            ],
        ),
    ]
